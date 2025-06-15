import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Times New Roman','SimSun']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# Simulate utilization for only 3 nodes
nodes_small = np.array([1, 2, 3])  # 3 nodes
pre_sched_utilization_small = [0.91, 0.5, 0.93]  # Skewed utilization for 3 nodes
post_sched_proposed_small = [0.72, 0.77, 0.7]  # Balanced utilization for proposed method
post_sched_lyra_small = [0.8, 0.6, 0.85]  # Lyra method
post_sched_pollux_small = [0.78, 0.65, 0.8]  # Pollux method

# Plotting pre-scheduling utilization
plt.figure(figsize=(10, 6))
plt.bar(nodes_small - 0.2, pre_sched_utilization_small, width=0.15, label="重调度触发前", color="red")
plt.bar(nodes_small, post_sched_proposed_small, width=0.15, label="本文方法重调度后", color="green")
plt.bar(nodes_small + 0.2, post_sched_lyra_small, width=0.15, label="Lyra 调度后", color="blue")
plt.bar(nodes_small + 0.4, post_sched_pollux_small, width=0.15, label="Pollux 调度后", color="purple")

# Chart details
plt.xlabel(u"节点编号",fontsize=14)
plt.ylabel(u"节\n点\nGPU\n利\n用\n率", rotation=0, labelpad=20, ha='left',fontsize=14, y=0.44)  # labelpad调整距离，ha调整对齐方式
plt.title(u"重调度前后节点 GPU 利用率对比",fontsize=16)
plt.xticks(nodes_small)
plt.ylim(0.4, 1.0)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

plt.show()
