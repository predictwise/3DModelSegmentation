__author__ = 'wlw'
# coding=utf-8
import numpy as np
import math, random, bisect


# 将以inch为单位的数据转换为以meter为单位
def realData(allTriPolygones):
    # 二维数组
    points = []
    for polygones in allTriPolygones:
        for polygone in polygones:
            for p in polygone:
                p[0] *= 0.0254
                p[1] *= 0.0254
                p[2] *= 0.0254
                points.append(p)

    return points


# 平移变换，polygones是三维数组
def translate(allTriPolygones):
    # 三角形顶点
    tri_points = realData(allTriPolygones)
    # 线的顶点
    line_points = realData(allTriPolygones)

    areas = []
    gravity = []
    # 所有三角形面积之和
    summ = 0
    for i in range(len(tri_points)/3):
        # 第i个三角形的面积
        a_pt = tri_points[i*3]
        b_pt = tri_points[i*3+1]
        c_pt = tri_points[i*3+2]
        s = getArea(a_pt, b_pt, c_pt)
        areas.append(s)
        summ += s

        # 第i个三角形的重心
        g = (a_pt+b_pt+c_pt) / 3.0
        gravity.append(g)


    mp = [0, 0, 0]
    for i in range(len(tri_points)/3):
        mp += areas[i] * gravity[i] / float(summ)

    print 'mp: ', mp

    # 开始平移模型，将重心作为空间原点
    transed_tripoints = []
    for point in tri_points:
        for i in range(3):
            point[i] -= mp[i]
        transed_tripoints.append(point)

    transed_linepoints = []
    for point in line_points:
        for i in range(3):
            point[i] -= mp[i]
        transed_linepoints.append(point)

    return mp, transed_tripoints, transed_linepoints


def getArea(a_pt, b_pt, c_pt):
    # 分别计算三角行三条边的长度
    d_ab = math.sqrt(sum(math.pow(a_pt[i]-b_pt[i], 2) for i in range(3)))
    d_bc = math.sqrt(sum(math.pow(b_pt[i]-c_pt[i], 2) for i in range(3)))
    d_ca = math.sqrt(sum(math.pow(c_pt[i]-a_pt[i], 2) for i in range(3)))

    # 利用海伦公式计算三角形的面积
    p = (d_ab + d_bc + d_ca) / 2.0
    s = 0
    try:
        # s = math.sqrt(p*(p-d_ab)*(p-d_bc)*(p-d_ca))
        s = math.sqrt(p*abs(p-d_ab)*abs(p-d_bc)*abs(p-d_ca))
    except:
        print d_ab
        print d_bc
        print d_ca
        print p
        print 's: ', s
    # print 's: ', s
    return s


# 蒙特卡洛法，需要知道重心
# 平移变换，polygones是三维数组
# def translate(allPolygones):
def translate2(polygones):
    # 二维数组
    points = []
    # for polygones in allPolygones:
    for polygone in polygones:
        for p in polygone:
            p[0] = p[0] * 0.0254
            p[1] = p[1] * 0.0254
            p[2] = p[2] * 0.0254
            points.append(p)

    # print 'points: ', points

    # 第i个元素是前i个三角形的面积之和，list的长度是所有三角形的个数
    areas = []
    summ = 0
    for i in range(len(points)/3):
        a_pt = points[i*3]
        b_pt = points[i*3+1]
        c_pt = points[i*3+2]
        s = getArea(a_pt, b_pt, c_pt)
        summ += s
        areas.append(summ)
    print 'areas: ', areas




    vertex_p = []
    '''
    for i in range(k):
        # 从0～所有三角形面积之和，之间生成一个随机数
        num = random.uniform(0, areas[len(points)-1])
        # 找到对应随机数的三角形的索引号
        tri_idx = bisect.bisect(areas, num)
        r1 = random.random()
        r2 = random.random()

        # 由索引号确定这个三角形的三个顶点
        p1 = points[tri_idx*3]
        p2 = points[tri_idx*3+1]
        p3 = points[tri_idx*3+2]

        # 这个三角形内部的一个采样点p
        p = (1-math.sqrt(r1))*p1 + math.sqrt(r1)*(1-r2)*p2 + math.sqrt(r1)*r2*p3
        vertex_p.append(p)
    '''
    return '111', '222'


# 面积加权法
# 平移变换，polygones是三维数组
def translate1(allPolygones):
    # 二维数组
    points = []
    for polygones in allPolygones:
        for polygone in polygones:
            for p in polygone:
                p[0] = p[0] * 0.0254
                p[1] = p[1] * 0.0254
                p[2] = p[2] * 0.0254
                # 增加一个flag，以防多次计算同一个顶点p的表面积
                p = np.append(p, 0)
                points.append(p)

    # print 'points: ', points

    # 重心
    mp = [0, 0, 0]
    # 去除了冗余的顶点
    for i in range(len(points)):
        box = []
        # 存放三角形的索引号
        tri_index = []
        # 存放所有与顶点p相关的三角形的面积
        areas = []

        for j in range(len(points)):
            # np.allclose(points[i], points[j]): 判断两者是否相等
            # flag=0代表还未被遍历到
            if points[j][3] == 0:
                if np.allclose(points[i][:3], points[j][:3]):
                    points[j][3] = 1
                    # print 'points[j][3]: ', points[j]
                    box.append(j)

        for k in box:
            # 是第几个三角形含有相同的顶点p
            tri_index.append(k/3)

        # 计算顶点p的表面积
        for idx in tri_index:
            a_pt = points[idx*3]
            b_pt = points[idx*3+1]
            c_pt = points[idx*3+2]
            s = getArea(a_pt, b_pt, c_pt)
            areas.append(s)

        # 顶点p的表面积, 作为顶点p的权重
        sp = (1/3.0)*sum(s for s in areas)
        for t in range(3):
            mp[t] += points[i][t] * sp

    # 开始平移模型，将重心作为空间原点
    transed_points = []
    for point in points:
        for i in range(3):
            point[i] -= mp[i]
        transed_points.append(point)

    # 去除transed_points中的flag, 下标为3, 恢复原状
    for i in range(len(transed_points)):
        transed_points[i] = np.delete(transed_points[i], 3)

    return mp, transed_points





