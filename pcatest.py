__author__ = 'wlw'
# coding:utf-8

import numpy
from sklearn import decomposition


# 构造聚类 类别数据
Data_Set = []
for k in range(5):
    arr = numpy.random.random([3000, 45])
    for i in numpy.arange(0, 3000):
        j = i % 3
        arr[i, k*9+j*3:k*9+j*3+3] = arr[i, k*9+j*3:k*9+j*3+3]+k*0.25
    print arr.shape
    Data_Set.append(arr)
Dim_Set = []
for Cat_Num in range(len(Data_Set)):
    pca = decomposition.PCA()
    pca.fit(Data_Set[Cat_Num])
    # 累计贡献率 又名 累计方差贡献率 不要简单理解为 解释方差！！！
    EV_List = pca.explained_variance_
    EVR_List = []
    for j in range(len(EV_List)):
        EVR_List.append(EV_List[j]/EV_List[0])

    Dim = 0
    for j in range(len(EVR_List)):
        if( EVR_List[j] < 0.10 ):
            Dim = j
            break
    Dim_Set.append(Dim)



Dim = max(Dim_Set)
print 'Dim: ', Dim
pca = decomposition.PCA(n_components=Dim, copy=True, whiten=False)
for k in range(len(Data_Set)):
    Data_Set[k] = pca.fit_transform(Data_Set[k])
    print 'Data_Set[k]: ', Data_Set[k]