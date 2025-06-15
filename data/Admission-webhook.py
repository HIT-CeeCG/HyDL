import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = ['Times New Roman','SimSun']

# Data for illegal traffic blocking rate experiment
illegal_traffic_ratios = np.linspace(10, 90, 9)  # Illegal traffic percentage
blocking_rates = [98.5, 98.6, 98.8, 99.0, 98.9, 99.1, 99.0, 99.2, 99.3]  # Blocking rates (%)

# Data for admission overhead experiment
task_types = ["ResNet50", "Bert", "GNMT16", "VGG"]
admission_overhead_ratios = [1.8, 2.1, 1.2, 1.5]  # Overhead as percentage of total task time

# Plot 1: Illegal traffic blocking rate
plt.figure(figsize=(8, 5))
plt.plot(illegal_traffic_ratios, blocking_rates, marker='o', linestyle='-', label='非法流量比例')
# plt.title('Illegal Traffic Blocking Rate')
plt.xlabel('非法流量比例 (%)',fontsize=14) 
plt.ylabel('阻\n拦\n比\n例\n(%)',fontsize=14,rotation=0, labelpad=30, ha='left') 
plt.grid(True)
plt.legend()
plt.show()

# Plot 2: Admission overhead experiment
plt.figure(figsize=(8, 5))
plt.bar(task_types, admission_overhead_ratios, color='skyblue')
# plt.title('Admission Overhead as Percentage of Task Time')
plt.xlabel('任务类型', fontsize=14)
plt.ylabel('判\n断\n时\n间\n占\nJCT\n比\n例\n(%)',fontsize=14,rotation=0, labelpad=30, ha='left')
plt.ylim(0, max(admission_overhead_ratios) + 1)
plt.grid(axis='y')
plt.show()
