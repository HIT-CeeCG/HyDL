## 一、介绍

本项目基于 QoS 机制，支持 Kubernetes 上多种工作负载的混部调度。它旨在提高工作负载的运行时效率和可靠性（包括延迟敏感型负载和批处理任务），简化资源相关的配置调优，增加 Pod 部署密度以提高资源利用率。

通过提供如下功能来增强用户在 Kubernetes 上管理工作负载的体验：

- 精心设计的 Priority 和 QoS 机制，支持在一个集群或者一个节点上混部不同的工作负载。
- 采用应用画像机制，支持超卖资源，以实现在满足 QoS 保障的前提下实现高资源利用率。
- 细粒度的资源编排和隔离机制以提高工作负载（包括延迟敏感型负载和批处理任务）的效率。
- 一套支持监控、故障排除、运维的工具集。



## 二、前言

- 项目基于 kubebuilder 构建，kubebuilder是一个构建 Kubernetes API 和 CRD 的 SDK，官方网站：[kubebuilder](https://github.com/kubernetes-sigs/kubebuilder)

- 关于 Kubernetes 和 kubebuilder 的快速上手知识，可以参考以下博客：[使用 kubebuilder 创建 operator 示例 · Kubernetes 中文指南——云原生应用架构实战手册 (jimmysong.io)](https://jimmysong.io/kubernetes-handbook/develop/kubebuilder-example.html)



## 三、项目目录介绍

`apis` 为通过 kubebuilder 生成的各个 CRD API 构建内容，包括集群配置、节点和pod的重新定义分类、runtime、scheduling和SLO划分定义

`cmd` 为几个主要组件的构建目录，通过 `docker` 目录的 `dockerfile` 将其中主要组件构建成镜像部署到相应节点上

`config` 为 kubebuilder 自动生成的 CRD 和 API 使用示例，不需要管

`pkg`  为各个组件定义内容的详细代码位置

`pkg/client` 工作节点侧相应各功能代码

`pkg/descheduler` 重调度相关代码

`pkg/koordlet` koordlet 组件代码

`pkg/runtimeproxy` 负责与kubelet通信，协调各组件间通信协议代码

`pkg/scheduler` 调度器相关代码，定义全部调度器初始协议

`pkg/slo-controller` SLO 控制器







## 四、GPU调度相关

1. 核心目的：
   1. 定义设备 CRD 和资源 API。
   2. 在 koordlet 中提供报告组件来报告设备信息和资源容量。
   3. 提供调度程序插件，支持用户以更细粒度申请 GPU 资源。
   4. 在 koordlet 中提供新的运行时hook插件，支持更新由调度程序分配的 GPU 的容器环境。

### 4.1 GPU 描述

将 GPU 资源抽象为不同的维度：

`kooperator/gpu-core` 表示 GPU 的计算能力。与 K8s MilliCPU 类似，将 GPU 的总计算能力抽象为一百，用户可以根据需要申请相应数量的 GPU 计算能力。
`kooperator/gpu-memory` 表示 GPU 的内存容量，单位为字节。
`kooperator/gpu-memory-ratio` 表示 GPU 内存的百分比。
假设节点 A 有 4 个 GPU 实例，每个实例的总内存为 8GB，当设备报告器向 Node.Status.Allocatable 上报 GPU 容量信息时，它不再报告 nvidia.com/gpu=4，而是报告以下信息：

```yaml
status:
  capacity:
    kooperator/gpu-core: 400
    kooperator/gpu-memory: "32GB"
    kooperator/gpu-memory-ratio: 400
  allocatable:
    kooperator/gpu-core: 400
    kooperator/gpu-memory: "32GB"
    kooperator/gpu-memory-ratio: 400
```

当用户申请 0.5/0.25 GPU 时，用户不知道每个 GPU 的确切内存总字节数，只想使用一半或四分之一的内存，因此用户可以使用 kooperator/gpu-memory-ratio 申请 GPU 内存。当调度程序在具体节点上分配 Pod 时，调度器将根据以下公式将 kooperator/gpu-memory-ratio 转换为 kooperator/gpu-memory：allocatedMemory = totalMemoryOf(GPU) * kooperator/gpu-memory-ratio，以便 GPU 隔离可以工作。

在调度过滤阶段，调度程序将对 kooperator/gpu-memory 和 kooperator/gpu-memory-ratio 进行特殊处理。当Pod指定kooperator/gpu-memory-ratio时，调度器会检查每个节点上的每个GPU实例是否有未分配或剩余的资源，以确保每个GPU实例上的剩余内存符合配比要求。

如果用户确切知道或可以粗略估计工作负载的具体内存消耗，则可以通过kooperator/gpu-memory申请GPU内存。所有详细信息可参见下文。

此外，当dimensity的值> 100时，表示Pod需要多设备。现在只允许该值除以100。

示例：用户申请设备资源场景

与`nvidia.com/gpu`兼容

```yaml
resources:
  requests:
    nvidia.com/gpu: "2"
    cpu: "4"
    memory: "8Gi"
```

调度程序将`nvida.com/gpu: 2`转换为以下规范：

```yaml
resources:
  requests:
    kooperator/gpu-core: "200"
    kooperator/gpu-memory-ratio: "200"
    kooperator/gpu-memory: "16Gi" # assume 8G memory in bytes per GPU
    cpu: "4"
    memory: "8Gi"
```

应用GPU全部资源或者部分资源

```yaml
resources:
   requests:
    kooperator/gpu: "50"
    cpu: "4"
    memory: "8Gi"
```

调度程序将`kooperator/gpu："50"`转换为以下规范：

```yaml
resources:
  requests:
    kooperator/gpu-core: "50"
    kooperator/gpu-memory-ratio: "50"
    kooperator/gpu-memory: "4Gi" # assume 8G memory in bytes for the GPU
    cpu: "4"
    memory: "8Gi"
```

分别应用`kooperator/gpu-core`和`kooperator/gpu-memory-ratio`

```yaml
resources:
  requests:
    kooperator/gpu-core: "50"
    kooperator/gpu-memory-ratio: "60"
    cpu: "4"
    memory: "8Gi"
```

分别应用`kooperator/gpu-core`和`kooperator/gpu-memory`

```yaml
resources:
  requests:
    kooperator/gpu-core: "60"
    kooperator/gpu-memory: "4Gi"
    cpu: "4"
    memory: "8Gi"
```

### 4.2 实现细节

#### 4.2.1 调度

1. 抽象新的数据结构来描述节点上每个设备的资源和健康状态。
2. 实现 Filter/Reserve/PreBind 扩展点。
3. 自动识别不同类型的设备。当添加新设备时，我们不需要修改任何代码

##### 4.2.2 DeviceAllocation

在 PreBind 阶段，调度程序会将设备（包括 GPU）的分配结果（包括设备的 Minor、ID、资源分配信息）以注释的形式更新到 Pod。

```go
/*
{
  "gpu": [
    {
      "minor": 0,
      "resources": {
        "kooperator/gpu-core": 100,
        "kooperator/gpu-memory-ratio": 100,
        "kooperator/gpu-memory": "16Gi"
      }
    },
    {
      "minor": 1,
      "resources": {
        "kooperator/gpu-core": 100,
        "kooperator/gpu-memory-ratio": 100,
        "kooperator/gpu-memory": "16Gi"
      }
    }
  ],
  "rdma": [
    {
      "minor": 0,
      "id": "0000:09:00.0",
      "resources": {
        "kooperator/rdma": 100,
      }
    },
    {
      "minor": 1,
      "id": "0000:10:00.0",
      "resources": {
        "kooperator/rdma": 100,
      }
    }
  ]
}
*/

type DeviceAllocation struct {
    Minor     int32               `json:"minor"`
    Resources corev1.ResourceList `json:"resources"`
    // ID is the well known identifier for device, because for some device, such as rdma, Minor is meaningless
    ID        string                     `json:"id,omitempty"`
    Extension *DeviceAllocationExtension `json:"extension,omitempty"`
}

type DeviceAllocations map[DeviceType][]*DeviceAllocation
```

##### 4.2.3 NodeDevicePlugin

```go
var (
	_ framework.PreFilterPlugin = &NodeDevicePlugin{}
	_ framework.FilterPlugin    = &NodeDevicePlugin{}
	_ framework.ReservePlugin   = &NodeDevicePlugin{}
	_ framework.PreBindPlugin   = &NodeDevicePlugin{}
)

type NodeDevicePlugin struct {
    frameworkHandler     framework.Handle
    nodeDeviceCache      *NodeDeviceCache
}

type NodeDeviceCache struct {
    lock        sync.Mutex
    nodeDevices map[string]*nodeDevice
}

type nodeDevice struct {
    lock        sync.Mutex
    DeviceTotal map[DeviceType]deviceResource
    DeviceFree  map[DeviceType]deviceResource
    DeviceUsed  map[DeviceType]deviceResource
    AllocateSet map[DeviceType]*corev1.PodList
}

// We use `deviceResource` to present resources per device.
// "0": {kooperator/gpu-core:100, kooperator/gpu-memory-ratio:100, kooperator/gpu-memory: 16GB}
// "1": {kooperator/gpu-core:100, kooperator/gpu-memory-ratio:100, kooperator/gpu-memory: 16GB}
type deviceResources map[int]corev1.ResourceList

```

将注册节点和设备事件处理程序来维护设备帐户。

- 在 Filter 中，将通过节点（gpu-memory 示例）组成每个设备请求，并尝试比较每个设备的可用资源和 Pod 设备请求。
- 在 Reserve/Unreserve 中，将更新 nodeDeviceCache 的已用/可用资源和 allocateSet。现在设备选择规则仅基于设备次要 ID 顺序。
- 在 PreBind 中，将 DeviceAllocations 写入 Pod 的注释。
- 在 Init 阶段，应该列出所有 Node/Device/Pod 以恢复设备帐户。

#### 4.2.4 Device Reporter

在 koordlet 中实现一个名为“Device Reporter”的新组件，用于创建或更新“Device”CRD 实例，其中包含每个设备的资源信息、拓扑信息、健康状态及其所属虚拟功能（包括 GPU等）。将执行“nccl”命令来获取每个次要资源，就像 k8s-gpu-device-plugins 一样。

### 4.3 Device CRD 方案定义

```go
type DeviceType string

const (
	GPU  DeviceType = "g
)

type DeviceSpec struct {
	Devices []DeviceInfo `json:"devices"`
}

type DeviceInfo struct {
    // Type represents the type of device
    Type DeviceType `json:"type,omitempty"`
    // Labels represents the device properties that can be used to organize and categorize (scope and select) objects
    Labels map[string]string `json:"labels,omitempty"`
    // UUID represents the UUID of device
    UUID string `json:"id,omitempty"`
    // Minor represents the Minor number of Device, starting from 0
    Minor *int32 `json:"minor,omitempty"`
    // ModuleID represents the physical id of Device
    ModuleID *int32 `json:"moduleID,omitempty"`
    // Health indicates whether the device is normal
    // +kubebuilder:default=false
    Health bool `json:"health"`
    // Resources is a set of (resource name, quantity) pairs
    Resources corev1.ResourceList `json:"resources,omitempty"`
    // Topology represents the topology information about the device
    Topology *DeviceTopology `json:"topology,omitempty"`
    // VFGroups represents the virtual function devices
    VFGroups []VirtualFunctionGroup `json:"vfGroups,omitempty"`
}

type DeviceTopology struct {
    // SocketID is the ID of CPU Socket to which the device belongs
    SocketID int32 `json:"socketID"`
    // NodeID is the ID of NUMA Node to which the device belongs, it should be unique across different CPU Sockets
    NodeID int32 `json:"nodeID"`
    // PCIEID is the ID of PCIE Switch to which the device is connected, it should be unique across difference NUMANodes
    PCIEID string `json:"pcieID"`
    // BusID is the domain:bus:device.function formatted identifier of PCI/PCIE device
    BusID string `json:"busID,omitempty"`
}

type VirtualFunctionGroup struct {
    // Labels represents the Virtual Function properties that can be used to organize and categorize (scope and select) objects
    Labels map[string]string `json:"labels,omitempty"`
	// VFs are the virtual function devices which belong to the group
    VFs []VirtualFunction `json:"vfs,omitempty"`
}

type VirtualFunction struct {
    // Minor represents the Minor number of VirtualFunction, starting from 0, used to identify virtual function.
    Minor int32 `json:"minor"`
    // BusID is the domain:bus:device.function formatted identifier of PCI/PCIE virtual function device
    BusID string `json:"busID,omitempty"`
}

type DeviceStatus struct {}

type Device struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   DeviceSpec   `json:"spec,omitempty"`
	Status DeviceStatus `json:"status,omitempty"`
}

type DeviceList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`

	Items []Device `json:"items"`
}
```

#### 4.3.1 CRD 示例

```yaml
apiVersion: scheduling.kooperator/v1alpha1
kind: Device
metadata:
  name: node-1
  annotations:
    node.kooperator/gpu-checkpoints: |-
      [
        {
          "podUID": "fa8983dc-bb76-4eeb-8dcc-556fbd44d7ce",
          "containerName": "cuda-container",
          "resourceName": "nvidia.com/gpu",
          "deviceIDs": ["GPU-36b27e44-b086-46f7-f2dc-73c36dc65991"]
        }
      ]
spec:
  devices:
  - health: true
    id: GPU-98583a5c-c155-9cf6-f955-03c189d3dbfb
    minor: 0
    resources:
      kooperator/gpu-core: "100"
      kooperator/gpu-memory: 15472384Ki
      kooperator/gpu-memory-ratio: "100"
    type: gpu
  - health: true
    id: GPU-7f6410b9-bdf7-f9a5-de09-aa5ec31a7124
    minor: 1
    resources:
      kooperator/gpu-core: "100"
      kooperator/gpu-memory: 15472384Ki
      kooperator/gpu-memory-ratio: "100"
    type: gpu
status: {}
```



### 4.4 koordlet 和 koord-runtime-proxy

这两个组件目标是兼容原始 k8s kubelet 和 k8s 设备插件，因此：

1. 仍然允许 kubelet 和设备插件分配具体设备，这意味着无论是否有 k8s 设备插件，这里的设计都可以正常工作。

2. 在 koord-runtime-proxy 中，将使用注释中的 Pod 的 `DeviceAllocation` 来替换步骤 1 的容器参数和环境结果。

此外应该修改 koord-runtime-proxy 和 koordlet 之间的协议以添加容器环境：

```go
type ContainerResourceHookRequest struct {  
    ....
    Env map[string]string
}

type ContainerResourceHookResponse struct {
    ....
    Env map[string]string
}
```

然后在koordlet的runtimehooks中添加一个新的`gpu-hook`，注册到`PreCreateContainer`阶段。

将根据Pod注释中的GPU分配结果生成新的GPU环境`NVIDIA_VISIBLE_DEVICES`。

koord-runtime-proxy可以看到这些Pod的环境，需要koord-runtime-proxy将这些环境传递给koordlet，koordlet解析GPU相关的环境以找到具体的设备id。

此外，koordlet应该将GPU模型报告给与设备插件相同的节点标签，以防在没有设备插件的情况下工作。

最后，应该修改koord-runtime-proxy中`ContainerResourceExecutor`的`UpdateRequest`函数，让新的GPU环境覆盖旧的GPU环境。

当处理热更新时，可以处理Pod注释中没有设备分配的现有调度Pod。如果 GPU 分配信息不在注释中，将从 `ContainerResourceHookRequest` 的 `Env` 中找到 GPU 分配，并将所有 GPU 分配更新到设备 CRD 实例。
