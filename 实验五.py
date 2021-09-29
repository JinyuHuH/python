
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data=pd.read_csv(r"E:\数据可视化\master.csv")
dt=pd.DataFrame(data)
print(dt.corr())
sns.heatmap(dt.corr())#相关性热力图
#sns.heatmap(dt.corr('kendall'))
#sns.heatmap(dt.corr('spearman'))
#sns.pairplot(dt,hue='sex')
#sns.pairplot(dt,hue='age')
#sns.pairplot(dt,hue='generation')
plt.show()

