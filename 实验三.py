from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator
plt.rcParams['font.sans-serif'] = ['SimHei']
dt=pd.read_excel("E:\桂林市1951-2014年月降水量.xlsx",header=0)
dt_clean =dt.iloc[0:,0:13]
#print(dt_clean)
#dt_static =(dt_clean.describe())
#years = dt_clean["月份"]
#plt.figure(figsize=(15,10),dpi=100)
#for i in range(1,13):
 #   y_values=dt_clean[i]
  #  mean_january = np.mean(y_values)
   # plt.subplot(6,2,i)
    #plt.plot(years,y_values,label="降雨量")
#    plt.plot(years,[mean_january for x in range(len(y_values))],label="均值")
 #   plt.xlabel("years")
  #  plt.ylabel("january")
   # plt.title("桂林市1951-2014年{}月份降雨趋势图".format(i))
    #plt.legend(loc=1)
#    y_locator = MultipleLocator(200)
 #   months = plt.gca()
  #  months.yaxis.set_major_locator(y_locator)
   # plt.subplots_adjust(hspace=0.8)
#plt.show()
lv1 = sum(np.sum(dt<10))
lv2 = sum(np.sum(dt<=25))
lv3 = sum(np.sum(dt<=50))
lv4 = sum(np.sum(dt<=100))
lv5 = sum(np.sum(dt<=250))
lv6 = sum(np.sum(dt<=1000))
x = ["小雨",'中雨','大雨','暴雨','大暴雨','特大暴雨']
fres = [lv1,lv2 - lv1,lv3 - lv2,lv4 - lv3,lv5 - lv4,lv6 - lv5]
plt.plot(range(len(x)),fres,c='g',linestyle='-')
plt.scatter(range(len(x)),fres,c='r',alpha=0.5,marker = "o",s = np.array(fres)*5)
for i_x,i_y in zip(range(len(x)),fres):
    plt.text(i_x,i_y,i_y,fontsize = 20)
plt.bar(range(len(x)),fres,fc = "b")
plt.xticks(range(len(x)),x) # 设置x轴刻度以及名称
plt.xlabel("降雨类型")
plt.ylabel("频次")
plt.title("桂林市1951-2014年降雨量类型频次图")
plt.show()