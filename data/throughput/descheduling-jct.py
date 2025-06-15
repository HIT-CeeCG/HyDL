import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Times New Roman','SimSun']  # 用来正常显示中文标签

# Simulated completion times for three methods: Proposed, Lyra, Pollux
methods = ["本文方法", "Lyra", "Pollux"]
resnet50_times = [628, 676, 643]  # ResNet-50 inference times for three methods
bert_times = [93, 126, 143]      # BERT inference times for three methods
vgg_times = [113, 134, 142]       # VGG inference times for three methods
gnmt16_times = [55, 60, 65]    # GNMT-16 inference times for three methods

# Plotting ResNet-50
plt.figure(figsize=(8, 6))
plt.bar(methods, resnet50_times, color=["green", "blue", "purple"])
plt.xticks(size=18)
plt.yticks(size=16)
plt.xlabel("方法",fontsize=18)
plt.ylabel("任\n务\n平\n均\n完\n成\n时\n间\n(ms)", rotation=0, labelpad=30, ha='left',fontsize=18, y=0.29)
plt.title("ResNet-50 推理任务重调度后平均完成时间对比",fontsize=18)
plt.ylim(600, 680)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Plotting BERT
plt.figure(figsize=(8, 6))
plt.bar(methods, bert_times, color=["green", "blue", "purple"])
plt.xticks(size=18)
plt.yticks(size=16)
plt.xlabel("方法",fontsize=18)
plt.ylabel("任\n务\n平\n均\n完\n成\n时\n间\n(ms)", rotation=0, labelpad=30, ha='left',fontsize=18, y=0.35)
plt.title("BERT 推理任务重调度后平均完成时间对比",fontsize=18)
plt.ylim(50, 150)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Plotting VGG
plt.figure(figsize=(8, 6))
plt.bar(methods, vgg_times, color=["green", "blue", "purple"])
plt.xticks(size=18)
plt.yticks(size=16)
plt.xlabel("方法",fontsize=18)
plt.ylabel("任\n务\n平\n均\n完\n成\n时\n间\n(ms)", rotation=0, labelpad=30, ha='left',fontsize=18, y=0.32)
plt.title("VGG 推理任务重调度后平均完成时间对比",fontsize=18)
plt.ylim(80, 150)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Plotting GNMT-16
plt.figure(figsize=(8, 6))
plt.bar(methods, gnmt16_times, color=["green", "blue", "purple"])
plt.xticks(size=18)
plt.yticks(size=16)
plt.xlabel("方法",fontsize=18)
plt.ylabel("任\n务\n平\n均\n完\n成\n时\n间\n(ms)", rotation=0, labelpad=30, ha='left',fontsize=18, y=0.29)
plt.title("GNMT-16 推理任务重调度后平均完成时间对比",fontsize=18)
plt.ylim(30, 70)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
