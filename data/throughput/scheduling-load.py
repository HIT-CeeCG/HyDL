# Re-importing necessary libraries after environment reset
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Times New Roman','SimSun']  # 用来正常显示中文标签


# Simulated scheduling overhead data
methods = ["本文方法", "Lyra", "Pollux"]
overhead = [7, 10, 15]  # Overhead as percentage of task completion time

# Plotting scheduling overhead
plt.figure(figsize=(8, 6))
plt.bar(methods, overhead, color=["green", "blue", "purple"])
plt.xlabel("方法对比",fontsize=14)
plt.ylabel("调\n度\n开\n销\n占\n比",fontsize=14,rotation=0, labelpad=20, ha='left')
plt.title(u"调度时间开销代价对比",fontsize=16)
plt.ylim(0, 20)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Adding value annotations
for i, value in enumerate(overhead):
    plt.text(i, value + 0.5, f"{value}%", ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.show()
