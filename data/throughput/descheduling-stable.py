# Re-importing necessary libraries
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = ['Times New Roman','SimSun']  # 用来正常显示中文标签


# Simulated data for four tasks
tasks = ["ResNet-50", "BERT", "VGG", "GNMT-16"]
impact_on_online = [5, 6, 4, 7]  # Percentage of online tasks affected by rescheduling
impact_on_inference = [6, 4, 3, 6]  # Percentage of inference tasks affected by rescheduling
rescheduling_needed = [2, 3, 2, 1]  # Percentage of offline tasks requiring second rescheduling

# Plotting the data for each task
x = np.arange(len(tasks))
bar_width = 0.2

plt.figure(figsize=(12, 8))
plt.bar(x - bar_width, impact_on_online, bar_width, label="影响的离线任务比例 (%)", color="blue")
plt.bar(x, impact_on_inference, bar_width, label="影响的在线任务比例 (%)", color="orange")
plt.bar(x + bar_width, rescheduling_needed, bar_width, label="需要二次重调度的离线任务比例 (%)", color="green")

# Chart details
plt.xlabel("任务",fontsize=15)
plt.ylabel("百\n分\n比",rotation=0, labelpad=20, ha='left',fontsize=15)
plt.title("重调度后任务稳定性分析",fontsize=16)
plt.xticks(x, tasks)
plt.legend()
plt.ylim(0, 10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

plt.show()
