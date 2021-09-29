import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import MultipleLocator
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def start_pca():
    # 第一步，构造原始数据矩阵(0,1),(1,0)
    x_values = [-1,-1,0,2,0]
    y_values = [-2,0,0,1,1]

    m_orgin = np.array([x_values,y_values])
    m_orgin_temp = m_orgin
    nrows,ncols = m_orgin.shape


    # 第二步：数值中心化，即变量值减去该属性的均值

    for row in range(nrows):
        ma = np.mean(m_orgin[row,:])
        m_orgin[row,:] = m_orgin[row,:] - ma
    # 第三步：求协方差矩阵
    c = (1/len(x_values))*m_orgin.dot(np.transpose(m_orgin))
    # 第四步：求特征值以及特征向量
    feature = np.linalg.eig(c) # 求矩阵的特征值以及特征向量
    print(feature)
    p = feature[1][0,:]
    plt.plot(p*30,p*30,linestyle ='--')
    k=1
    b=0
    for i in range(nrows):
        x=(k*y_values[i]+x_values[i]-k*b)/(k**2+1)
        y=(k**2*y_values[i]+k*x_values[i]+b)/(k**2+1)
        plt.scatter(x,y)
        plt.plot([x_values[i],x],[y_values[i],y],linestyle ='--')


    draw_pca(x_values, y_values)
    m_after = np.array(p).dot(m_orgin_temp)
    print(m_after)



def draw_pca(x_values,y_values):
    ax = plt.gca() # 获得图表的坐标对象
    # 去掉坐标轴的对应边框
    ax.spines['top'].set_color('none') #
    ax.spines['right'].set_color('none')  #

    # 设置坐标轴范围
    plt.xlim(-10,11)
    plt.ylim(-10,11)

    # 设置坐标轴的刻度
    x_multi = MultipleLocator(1) # 步长为1的刻度
    y_multi = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_multi)
    ax.yaxis.set_major_locator(y_multi)


    # 设置坐标轴原点
    ax.spines['bottom'].set_position(('data',0))
    ax.spines['left'].set_position(('data', 0))

    # 设置箭头
    ax.arrow(0,-10,0,20,length_includes_head = False,head_width = 0.75,overhang = 1)
    # length_includes_head = True 箭头是否在你的计算长度之内
    ax.arrow(-10,0, 20, 0,length_includes_head = False,head_width = 0.75,overhang = 1)


    plt.scatter(x_values,y_values,marker='*',c='r')
    plt.show()



if __name__ == '__main__':
    start_pca()