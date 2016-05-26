__author__ = 'wlw'
# coding=utf-8

import math


# 缩放变换
def scale(mp, transed_tripoints):
    max_dist = 0
    for p in transed_tripoints:
        dist = math.sqrt(sum(math.pow(p[i]-mp[i], 2) for i in range(3)))
        if max_dist < dist:
            max_dist = dist

    # 缩放系数
    max_dist = float(max_dist)
    k = 1 / max_dist
    print 'k: ', k

    # 最终三角形的顶点
    final_tripoints = []
    for point in transed_tripoints:
        for i in range(3):
            point[i] *= k
        final_tripoints.append(point)

    return final_tripoints

