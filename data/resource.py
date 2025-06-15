import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = ['Times New Roman','SimSun']

hours = np.arange(0, 24, 0.25)  # Every 15 minutes for 24 hours

# Generating various resource data
total_allocable_resource_line = np.full(hours.shape, 80)  # Fixed Total Allocable Resource Line at 70%
actual_allocated_resources = np.random.normal(loc=60, scale=5, size=hours.shape)  # Actual allocated resources
requested_resource_total_adjusted = actual_allocated_resources - np.random.uniform(5, 10, size=hours.shape)
long_term_reservation_adjusted = requested_resource_total_adjusted - np.random.uniform(10, 15, size=hours.shape)
actual_resource_usage = np.random.normal(loc=35, scale=5, size=hours.shape)
short_term_reservation_adjusted = actual_resource_usage + np.random.normal(5, 7, size=hours.shape)

# Creating the plot
plt.figure(figsize=(13, 10))
plt.axhline(y=70, color='blue', linestyle='-', linewidth=1.5, label='limit: 请求资源总量(70%)')
plt.axhline(y=80, color='red', linestyle='-', linewidth=1.5, label='total: 可分配资源总量(80%)')
# plt.axhline(y=np.mean(requested_resource_total_adjusted), color='orange', linestyle='-', linewidth=1.5, label='Requested Resource Total Line')
plt.axhline(y=60, color='green', linestyle='-', linewidth=1.5, label='long-term reservation: long-term资源使用预估')
plt.plot(hours, short_term_reservation_adjusted, '--', label='short-term reservation: short-term资源使用预估', linewidth=2)
plt.plot(hours, actual_resource_usage, label='usage: 实际资源使用', linewidth=2)

# Adding details to the plot
# plt.title('Corrected Time Series Analysis of System Resource Allocation')
plt.xlabel('时间（小时）',fontsize=14)
plt.ylabel('资\n源\n利\n用\n率\n(%)',fontsize=14,rotation=0, labelpad=20, ha='left')
plt.xticks(np.arange(0, 25, 1))  # Hour marks
plt.yticks(np.arange(0, 101, 10))  # Percentage marks
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=14)
plt.legend(loc='upper left', fontsize=14)


plt.tight_layout()

# Show the plot
plt.show()
