import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 示例数据集
data = {
    'Application': ['ResNet50', 'BERT', 'GNMT16', 'VGG'],
    'Kooperator_Queueing_Time': [3296, 1872, 6893, 309],
    'Baseline_Queueing_Time': [4592, None, None, None],
    'Kooperator_JCT': [12032, 6349, 26842, 162],
    'Baseline_JCT': [19872, None, None, None],
    'Kooperator_GPU_Usage': [0.88, 0.81, 0.83, 0.87],
    'Baseline_GPU_Usage': [0.75, None, None, None],
}

df = pd.DataFrame(data)

# 排队时间比较图
plt.figure(figsize=(10, 6))
sns.barplot(x='Application', y='Kooperator_Queueing_Time', data=df, color='lightblue', label='Kooperator')
sns.barplot(x='Application', y='Baseline_Queueing_Time', data=df, color='lightcoral', label='Baseline')
plt.title('Queuing Time Comparison')
plt.ylabel('Queuing Time (s)')
plt.legend()
plt.tight_layout()
plt.show()

# 任务完成时间比较图
plt.figure(figsize=(10, 6))
sns.barplot(x='Application', y='Kooperator_JCT', data=df, color='lightblue', label='Kooperator')
sns.barplot(x='Application', y='Baseline_JCT', data=df, color='lightcoral', label='Baseline')
plt.title('Job Completion Time (JCT) Comparison')
plt.ylabel('Job Completion Time (s)')
plt.legend()
plt.tight_layout()
plt.show()

# GPU 利用率比较图
plt.figure(figsize=(10, 6))
sns.barplot(x='Application', y='Kooperator_GPU_Usage', data=df, color='lightblue', label='Kooperator')
sns.barplot(x='Application', y='Baseline_GPU_Usage', data=df, color='lightcoral', label='Baseline')
plt.title('GPU Utilization Comparison')
plt.ylabel('GPU Utilization')
plt.legend()
plt.tight_layout()
plt.show()
