import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
config = {
        "font.family": 'serif',
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['SimSun'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
rcParams.update(config)


# Data from the provided table
data = {
    'Method': ['Baseline', 'Our Method', 'Lyra', 'Pollux'],
    'CPU Usage (Training)': [0.77, 0.81, 0.80, 0.76],
    'CPU Usage (Overall)': [0.33, 0.76, 0.69, 0.65],
    'Memory Usage (Training)': [0.65, 0.70, 0.68, 0.60],
    'Memory Usage (Overall)': [0.41, 0.65, 0.60, 0.50],
    'GPU Usage (Training)': [0.75, 0.88, 0.86, 0.84],
    'GPU Usage (Overall)': [0.42, 0.75, 0.69, 0.77]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Plotting the data for comparison
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

# CPU Usage Comparison
x = np.arange(len(df['Method']))
width = 0.2

axes[0].bar(x - width, df['CPU 使用率（训练任务）'], width, label='CPU 使用率（训练任务）')
axes[0].bar(x, df['CPU 使用率（混部）'], width, label='CPU 使用率（混部）')
axes[0].set_xticks(x)
axes[0].set_xticklabels(df['Method'])
axes[0].set_title('CPU Usage Comparison for ResNet50')
axes[0].set_ylabel('Usage')
axes[0].legend()
axes[0].grid(axis='y', linestyle='--', alpha=0.7)



# # Memory Usage Comparison
# axes[1].bar(x - width, df['Memory Usage (Training)'], width, label='Memory Usage (Training)')
# axes[1].bar(x, df['Memory Usage (Overall)'], width, label='Memory Usage (Overall)')
# axes[1].set_xticks(x)
# axes[1].set_xticklabels(df['Method'])
# axes[1].set_title('Memory Usage Comparison for ResNet50')
# axes[1].set_ylabel('Usage')
# axes[1].legend()
# axes[1].grid(axis='y', linestyle='--', alpha=0.7)


# # GPU Usage Comparison
# axes[2].bar(x - width, df['GPU Usage (Training)'], width, label='GPU Usage (Training)')
# axes[2].bar(x, df['GPU Usage (Overall)'], width, label='GPU Usage (Overall)')
# axes[2].set_xticks(x)
# axes[2].set_xticklabels(df['Method'])
# axes[2].set_title('GPU Usage Comparison for ResNet50')
# axes[2].set_ylabel('Usage')
# axes[2].legend()
# axes[2].grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
