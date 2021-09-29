import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
color = plt.cm.Spectral(np.linspace(0, 1, 22))  # 颜色设置
from collections import Counter
import json
# def ts(str):
#   url = "http://fanyi.youdao.com/openapi.do?keyfrom=orchid&key=1008797533&type=data&doctype=json&version=1.1&q={}".format(
#       str)
#  response = requests.post(url)
# if response.status_code == 200:
#    return json.loads(response.text)
def sex(data):#饼图
    # 筛选数据集
    data_0 = data[data['sex'] == 'female']
    data_1 = data[data['sex'] == 'male']
    total = data_0['suicides_no'].values.sum() + data_1['suicides_no'].values.sum()
    # 求占比
    female = data_0['suicides_no'].values.sum() / total
    male = data_1['suicides_no'].values.sum() / total
    plt.title('男女自杀比例')
    x = ['女性', '男性']
    y = [female, male]
    plt.pie(y, labels=x, autopct='%2.0f%%')  # 设置占比，x值
    plt.show()


def age(data):#折线图
    # 筛选数据集
    data1 = data[data['age'] == '5-14 years']
    data2 = data[data['age'] == '15-24 years']
    data3 = data[data['age'] == '25-34 years']
    data4 = data[data['age'] == '35-54 years']
    data5 = data[data['age'] == '55-74 years']
    data6 = data[data['age'] == '75+ years']
    # 求各年龄段每年平均自杀率
    suicide1 = (data1['suicides/100k pop'].groupby(data1['year']).sum() / data1[
        'year'].value_counts().sort_index().values).tolist()
    suicide2 = (data2['suicides/100k pop'].groupby(data2['year']).sum() / data2[
        'year'].value_counts().sort_index().values).tolist()
    suicide3 = (data3['suicides/100k pop'].groupby(data3['year']).sum() / data3[
        'year'].value_counts().sort_index().values).tolist()
    suicide4 = (data4['suicides/100k pop'].groupby(data4['year']).sum() / data4[
        'year'].value_counts().sort_index().values).tolist()
    suicide5 = (data5['suicides/100k pop'].groupby(data5['year']).sum() / data5[
        'year'].value_counts().sort_index().values).tolist()
    suicide6 = (data6['suicides/100k pop'].groupby(data6['year']).sum() / data6[
        'year'].value_counts().sort_index().values).tolist()
    suicide1.append(0)
    x = data5['suicides/100k pop'].groupby(data5['year']).sum().index.tolist()  # 年份集
    plt.plot(x, suicide1, label='5-14岁')
    plt.plot(x, suicide2, label='15-24岁')
    plt.plot(x, suicide3, label='25-34岁')
    plt.plot(x, suicide4, label='35-54岁')
    plt.plot(x, suicide5, label='55-74岁')
    plt.plot(x, suicide6, label='75+岁')
    plt.xlabel('年份')
    plt.ylabel('每年平均自杀率(suicides/100k)')
    plt.legend(loc=1)  # 图例
    plt.title('不同年龄段自杀率概况')
    plt.show()


def gdp_capita(data):#散点图
    data_new = data.pivot_table(values=['suicides/100k pop', 'gdp_per_capita ($)'], index=['country', 'year'])
    plt.title('人均GDP对自杀率影响')
    plt.scatter(x="gdp_per_capita ($)", y="suicides/100k pop", data=data_new, marker="o",color=color[13])  # 散点图图表设置
    plt.xlabel('人均GDP')
    plt.ylabel('自杀率(suicides/100k)')
    plt.show()


def country(data):#柱形图
    data.groupby(['country']).suicides_no.mean().nlargest(10).plot(kind='bar', color=color)  # 筛选国家
 #   print(data.groupby(['country']).suicides_no.mean().nlargest(10))
    plt.ylabel('平均自杀人数')
    plt.xlabel('国家')
    plt.title('自杀人数的平均值最高的前10个国家')
    plt.show()


def generation(data):#圆形雷达图
    data['generation_suicides_no'] = data['suicides_no'].groupby(data['generation']).cumsum()#累积求各年代自杀总数并创建新列
    last_data= data.drop_duplicates(subset=['generation'], keep='last')#保留最后数据
    print(last_data)
    suicide_num = last_data['generation_suicides_no'].values.tolist()#各年代自杀数集
    labels=last_data['generation'].values.tolist()#年代集
    dataLenth=6#数据长度
    angles=np.linspace(0,2*np.pi,dataLenth,endpoint=False)
    values=np.concatenate((suicide_num,[suicide_num[0]]))#闭合
    angles=np.concatenate((angles,[angles[0]]))#闭合
    plt.polar(angles,values,'bo-')
    plt.thetagrids(angles*180/np.pi,labels)#设置角度值
    plt.fill(angles,values,facecolor='r',alpha=0.25)#填充区域
    plt.ylim(0,2500000)#设置最大值区域
    plt.title('各年代自杀人数对比')
    plt.show()

if __name__ == '__main__':
    dt = pd.read_csv(r"E:\数据可视化\master.csv")
#    sex(dt)#男女自杀比例
#    age(dt)  # 不同年龄段自杀率概况
#    country(dt)# 自杀人数的平均值最高的前10个国家
#    gdp_capita(dt)#人均gdp对自杀率影响
    generation(dt)#各年代自杀人数对比
