__author__ = 'wlw'
# coding=utf-8
import numpy as np
from sklearn.decomposition import PCA
from shapely.geometry import *


# pts是降至二维后的数据, 计算由pts围成的二维区域的面积
def PolyArea2D(pts):
    # hstack: 横着合并数组
    lines = np.hstack([pts, np.roll(pts, -1, axis=0)])
    # print 'lines: ', lines
    area = 0.5*abs(sum((x1*0.0254)*(y2*0.0254)-(x2*0.0254)*(y1*0.0254) for x1, y1, x2, y2 in lines))
    return area


# 计算由二维坐标点集合points围成的凸多边形convex hull的面积大小
def getCVXarea(points):
    # print 'getCVXarea',ps
    tcs = []
    for t in points:
        tcs.append([t[0], t[1], 0])
    mp = MultiPoint(tcs)
    cx = mp.convex_hull
    # print cx.area
    return cx.area


# 默认方差百分比=99%
def pcagen(polygones, dv=0.99):
    # print 'polygones: ', polys
    l = len(polygones)
    print 'l: ', l

    if l > 3000 or l <= 0:
        return []
        pass

    # 主成分方差百分比
    pca_percent = np.zeros((l, l), dtype=float)
    # 面积
    area = np.zeros((l, l), dtype=float)
    for i in range(l):
        for j in range(i, l):
            if i == j:
                # 对数组的操作
                pca_percent[i, j] = 0
                area[i, j] = 0
                continue
            # 一个三角形三个顶点的坐标
            pi = polygones[i]
            # print 'pi: ', pi

            # 一个三角形三个顶点的坐标
            pj = polygones[j]
            # print 'pj: ', pj

            p = []
            # extend()方法只接受一个list作为参数，并将该参数的每个元素都添加到原有的列表中
            p.extend(pi)
            p.extend(pj)
            # 此时的p是一个6x3的二维数组，存放两个三角形，每一行是一个三角形顶点的（x,y,z）值

            # 设置将3D->2D数据
            pca = PCA(n_components=2)
            # fit(p)，表示用数据p来训练PCA模型
            pca.fit(p)
            # 将数据pi（三维数据）转换成降维后的数据pi2（二维数据）
            pi2 = pca.transform(pi)
            pj2 = pca.transform(pj)

            # analysis(pi,pj)

            # 存放下标为i的降维之后的三角形面积，与，下标为j的降维之后的三角形面积，之差
            area[i, j] = PolyArea2D(pi2)-PolyArea2D(pj2)
            # print 'area[i, j]: ', area[i, j]
            # 返回所保留的2个主成分各自的方差百分比之和
            pca_percent[i, j] = pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]
            # print 'pca_percent[i, j]: ', pca_percent[i, j]

    rem = []
    deles = []
    while pca_percent.max() > dv:
        if len(rem) > len(polygones)-5:  # 为什么要减5？
            break
        # pcas.argmax()：得到一个数组中最大元素的位置，e.g. np.array([[10,50,30],[60,20,40]])最大元素的位置为3
        # pcas.shape返回pcas数组的规模（行数x列数）, 是一个元组
        # unravel_index(pcas.argmax(), pcas.shape)，以元组的形式返回主成分百分比的位置, 对应上面的例子为(1,0)
        i, j = np.unravel_index(pca_percent.argmax(), pca_percent.shape)

        # 是由下标为i和j的两个三角行共同导致这一最大的主成分百分比
        # 百分比超过了0.99，所以要继续用pca处理
        pi = polygones[i]
        pj = polygones[j]

        p = []
        p.extend(pi)
        p.extend(pj)
        pca = PCA(n_components=2)
        pca.fit(p)
        pi2 = pca.transform(pi)
        pj2 = pca.transform(pj)

        # p2为6x2数组
        p2 = pca.transform(p)

        # analysis(pi,pj) 计算出经过pca变换后pi,pj及其点集的凸多边形的面积
        area_pi = PolyArea2D(pi2)
        area_pj = PolyArea2D(pj2)
        # 计算由二维坐标点集合p2围成的凸多边形convex hull的面积大小
        area_p2 = getCVXarea(p2)
        # print 'pca area:', area_p2, area_pi, area_pj

        if area_p2 > max(area_pi, area_pj)*1.3:  # 如果凸多边形面积ap2大于最大面积的1.3倍，则不进行删除
            # print 'if pca area:',ap2,api,apj
            pca_percent[i, j] = 0
            continue
        if area[i, j] > 0:
            # print 'pca_percent:',pca_percent[i,:].max(), pca_percent[j,:].max()
            if j not in rem:
                rem.append(j)
                deles.append((j, i, area_pj, area_pi, area_p2, pca_percent[j, i]))
                for k in range(l):
                    pca_percent[k, j] = 0
                    pca_percent[j, k] = 0

        else:
            if i not in rem:
                rem.append(i)
                deles.append((i, j, area_pi, area_pj, area_p2, pca_percent[i, j]))
                for k in range(l):
                    pca_percent[k, i] = 0
                    pca_percent[i, k] = 0
        pca_percent[i, j] = 0
        pca_percent[j, i] = 0

        #print pcas.max()
        #print pcas
    #print len(rem)
    print 'rem: ', rem
    print 'deles: ', deles
    newpolys = []
        #print 'rem:',rem

    for i in range(len(polygones)):
        if i not in rem:
            newpolys.append(polygones[i])

    return newpolys

