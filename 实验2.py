import numpy as np
#p1=(1,2,3)
#p2=(4,5,6)
#vec1 = np.array(p1)
#vec2 = np.array(p2)
#Euclidean_distance= np.sqrt(np.sum(np.square(vec1-vec2)))
#print("欧式距离为：",Euclidean_distance)
#Manhattan_distance=sum(abs(vec1-vec2))
#print("曼哈顿距离为：",Manhattan_distance)
#Chebyshev_distance=abs(vec1-vec2).max()
#print("切比雪夫距离为：",Chebyshev_distance)
#print("闵可夫斯基距离为")
#if len(vec1) == 1:
  #  print(Manhattan_distance)
#elif len(vec1) == 2:
  #  print(Euclidean_distance)
#else:
 #   print(Chebyshev_distance)


#Minkowski_distance=
#cos= 1 - np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
#print("余弦相似度为：",cos)
import numpy as np
#x = np.random.random(10)
#y = np.random.random(10)
# 马氏距离要求样本数要大于维数，否则无法求协方差矩阵
# 此处进行转置，表示10个样本，每个样本2维
X = np.vstack([x, y])
XT = X.T
#S = np.cov(X)  # 两个维度之间协方差矩阵
#SI = np.linalg.inv(S)  # 协方差矩阵的逆矩阵
# 马氏距离计算两个样本之间的距离，此处共有10个样本，两两组合，共有45个距离。
#n = XT.shape[0]
#mahalanobis_distance= []
#for i in range(0, n):
 #   for j in range(i + 1, n):
  #      delta = XT[i] - XT[j]
   #     d = np.sqrt(np.dot(np.dot(delta, SI), delta.T))
    #    mahalanobis_distance.append(d)
#print('马氏距离为:', mahalanobis_distance)
#import numpy as np

x=np.random.random(10)
y=np.random.random(10)
x_=x-np.mean(x)
y_=y-np.mean(y)
#pearson=np.dot(x_,y_)/(np.linalg.norm(x_)*np.linalg.norm(y_))
#print('皮尔逊相似度为:', pearson)
X = np.vstack([x, y])
d2 = pdist(X, 'jaccard')
vector1 = np.array([1, 3])
vector2 = np.array([4, 6])
funt(vector1, vector2)