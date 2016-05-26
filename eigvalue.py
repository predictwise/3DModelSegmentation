__author__ = 'wlw'
# coding=utf-8
import numpy as np
import math


def extractXOY(final_points):
    # 去除重复的顶点，只保留一个
    res = {point.tostring(): point for point in final_points}
    duped_points = res.values()
    x = []
    y = []

    # for p in final_points:
    for p in duped_points:
        x.append(p[0])
        y.append(p[1])

    max_x = max(x)
    min_x = min(x)
    range_x = abs(max_x - min_x)
    max_y = max(y)
    min_y = min(y)
    range_y = abs(max_y - min_y)

    # 包围圆的半径
    r = math.sqrt(math.pow(range_x, 2)+math.pow(range_y, 2))*0.5
    #print 'extractXOY r: ', r
    # 包围圆的圆心
    o = [0.5*(max_x+min_x), 0.5*(max_y+min_y)]
    #print 'len(duped_points): ', len(duped_points)
    # 存放每一个扇形区域中离圆心距离最远点的距离
    maxs_xoy = np.zeros(24, dtype=float)
    for i in range(len(duped_points)):
        # 第一个参数为对边边长， 第二个参数为临边边长
        degree = math.atan2(y[i]-o[1], x[i]-o[0])*180 / math.pi
        flag = judgedegree(degree)
        dist = math.sqrt(math.pow(x[i]-o[0], 2)+math.pow(y[i]-o[1], 2))
        if maxs_xoy[flag] < dist:
            maxs_xoy[flag] = dist

    #print 'maxs_xoy: ', maxs_xoy
    return maxs_xoy


def extractXOZ(final_points):
    # 去除重复的顶点，只保留一个
    res = {point.tostring(): point for point in final_points}
    duped_points = res.values()
    x = []
    z = []

    # for p in final_points:
    for p in duped_points:
        x.append(p[0])
        z.append(p[2])

    max_x = max(x)
    min_x = min(x)
    range_x = abs(max_x - min_x)
    max_z = max(z)
    min_z = min(z)
    range_z = abs(max_z - min_z)

    # 包围圆的半径
    r = math.sqrt(math.pow(range_x, 2)+math.pow(range_z, 2))*0.5
    #print 'extractXOZ r: ', r
    # 包围圆的圆心
    o = [0.5*(max_x+min_x), 0.5*(max_z+min_z)]
    #print 'len(duped_points): ', len(duped_points)
    # 存放每一个扇形区域中离圆心距离最远点的距离
    maxs_xoz = np.zeros(24, dtype=float)
    for i in range(len(duped_points)):
        # 第一个参数为对边边长， 第二个参数为临边边长
        degree = math.atan2(z[i]-o[1], x[i]-o[0])*180 / math.pi
        flag = judgedegree(degree)
        dist = math.sqrt(math.pow(x[i]-o[0], 2)+math.pow(z[i]-o[1], 2))
        if maxs_xoz[flag] < dist:
            maxs_xoz[flag] = dist

    #print 'maxs_xoz: ', maxs_xoz
    return maxs_xoz


def extractYOZ(final_points):
    # 去除重复的顶点，只保留一个
    res = {point.tostring(): point for point in final_points}
    duped_points = res.values()
    z = []
    y = []

    # for p in final_points:
    for p in duped_points:
        z.append(p[2])
        y.append(p[1])

    max_z = max(z)
    min_z = min(z)
    range_x = abs(max_z - min_z)
    max_y = max(y)
    min_y = min(y)
    range_y = abs(max_y - min_y)

    # 包围圆的半径
    r = math.sqrt(math.pow(range_x, 2)+math.pow(range_y, 2))*0.5
    #print 'extractYOZ r: ', r
    # 包围圆的圆心
    o = [0.5*(max_z+min_z), 0.5*(max_y+min_y)]
    #print 'len(duped_points): ', len(duped_points)
    # 存放每一个扇形区域中离圆心距离最远点的距离
    maxs_yoz = np.zeros(24, dtype=float)
    for i in range(len(duped_points)):
        # 第一个参数为对边边长， 第二个参数为临边边长
        degree = math.atan2(z[i]-o[0], y[i]-o[1])*180 / math.pi
        flag = judgedegree(degree)
        dist = math.sqrt(math.pow(z[i]-o[0], 2)+math.pow(y[i]-o[1], 2))
        if maxs_yoz[flag] < dist:
            maxs_yoz[flag] = dist

    #print 'maxs_yoz: ', maxs_yoz
    return maxs_yoz



def judgedegree(degree):
    # 每隔15度为一个扇形区, 共24个
    if degree >= 0 and degree < 15:
        return 0
    elif degree >= 15 and degree < 30:
        return 1
    elif degree >= 30 and degree < 45:
        return 2
    elif degree >= 45 and degree < 60:
        return 3
    elif degree >= 60 and degree < 75:
        return 4
    elif degree >= 75 and degree < 90:
        return 5
    elif degree >= 90 and degree < 105:
        return 6
    elif degree >= 105 and degree < 120:
        return 7
    elif degree >= 120 and degree < 135:
        return 8
    elif degree >= 135 and degree < 150:
        return 9
    elif degree >= 150 and degree < 165:
        return 10
    elif degree >= 165 and degree < 180:
        return 11
    elif degree >= -180 and degree < -165:
        return 12
    elif degree >= -165 and degree < -150:
        return 13
    elif degree >= -150 and degree < -135:
        return 14
    elif degree >= -135 and degree < -120:
        return 15
    elif degree >= -120 and degree < -105:
        return 16
    elif degree >= -105 and degree < -90:
        return 17
    elif degree >= -90 and degree < -75:
        return 18
    elif degree >= -75 and degree < -60:
        return 19
    elif degree >= -60 and degree < -45:
        return 20
    elif degree >= -45 and degree < -30:
        return 21
    elif degree >= -30 and degree < -15:
        return 22
    elif degree >= -15 and degree < 0:
        return 23