__author__ = 'wlw'
# coding=utf-8

import numpy as np


def rotate(transed_points):
    '''
    # 去除重复的顶点，只保留一个
    res = {point.tostring(): point for point in transed_points}
    duped_points = res.values()
    #print 'duped_points: ', duped_points
    '''

    # 旋转变换公式：M2=M1xR
    # R：旋转矩阵；M1：旋转前相关矩阵；M2：旋转后相关矩阵
    M1 = transed_points
    tmp = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)
    for point in M1:
        # point形如：[[-2892.76757812    62.03512573   587.66040039]]
        # point: 1x3
        point = point[np.newaxis]
        # 3x1, point的转置矩阵
        t_point = point.T
        # dot：叉乘
        tmp += np.dot(t_point, point)

    # 协方差矩阵
    n = float(len(M1))
    # *:点乘,得到协方差矩阵
    Cp = (1/n)*tmp
    # 计算特征值特征向量
    eVals, eVects = np.linalg.eig(Cp)
    # 对特征值从大到小排序，返回下标
    eVals_idx = np.argsort(-eVals)
    # 最大的3个特征值的下标，这里只有3个
    eValIdx = eVals_idx[0:3]
    # 旋转矩阵
    R = eVects[:, eValIdx]
    M2 = np.dot(M1, R)
    # print 'M2: ', M2
    return M2

