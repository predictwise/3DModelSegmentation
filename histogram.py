__author__ = 'wlw'
# coding=utf-8

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sympy import *


def getHist(allgeo, resx=1000, resy=1000):
    # 每一列的最小值
    minxyz = allgeo.min(axis=0)
    # 每一列的最大值
    maxxyz = allgeo.max(axis=0)
    dx = maxxyz[0]-minxyz[0]
    dy = maxxyz[1]-minxyz[1]
    dz = maxxyz[2]-minxyz[2]
    res = np.zeros((resx+1, resy+1))
    for r in allgeo:
        x = int(resx*(r[0]-minxyz[0])/dx)
        y = int(resy*(r[1]-minxyz[1])/dy)
        z = int(255*(r[2]-minxyz[2])/dz)
        # print z
        if z > res[x, y]:
            res[x, y] = z
    # print res
    #matplotlib.image.imsave('name.png', res)
    plt.imshow(res)
    plt.savefig('name.png')


def getTriHist(allTris, allgeo, name, resx, resy):
    print 'getTriHist'
    minxyz = allgeo.min(axis=0)
    maxxyz = allgeo.max(axis=0)
    dxyz = maxxyz-minxyz
    dv = np.array([resx+1, resy+1, 255])
    res = np.zeros((resx+1, resy+1))

    for tri in allTris:
        # //：取整除 - 返回商的整数部分
        t = (tri-minxyz)*dv//dxyz
        zv = getZvalue(t)
        for z in zv:
            if res[z[0], z[1]] < z[2]:
                res[z[0], z[1]] = z[2]

    #matplotlib.image.imsave('nametri.png', res)
    plt.imshow(res)
    plt.savefig('/home/wlw/wh3d/histogram/'+name+'.png')


def getZvalue(tri):
    res = []
    if tri.shape == (3, 3):
        tmin = tri.min(axis=0)
        tmax = tri.max(axis=0)
        #print 'tri2:', tri
        # touch(tri,None)
        for i in range(int(tmin[0]), int(tmax[0])):
            s, e = touch(tri, i, int(tmin[1]), int(tmax[1]))
            for j in range(s, e):
                res.append([i, j, getPanel(tri, i, j)])

    elif tri.shape == (2, 3):
        print 'line'
    return res


def touch(tri, x, y0, y1):
    ls1 = tri[0:2]
    ls2 = tri[1:]
    ls3 = tri[0:3:2]
    f = 0
    s = -1
    e = -1
    #print 'touch:',ls1,ls2,ls3,x,y0,y1
    for y in range(y0, y1+1):
        c = np.array([x, y])
        if online(ls1, c) or online(ls2, c) or online(ls3, c):
            if f == 0:
                s = y
                f = 1
            elif f == 1:
                e = y
            if f == 2:
                e = y
            if f == 1:
                pass
        elif f == 1:
            f = 2

    if f == 1:
        e = y1
    elif f == 2:
        pass
    else:
        e = s + 1
    # print 's,e: ', s, e
    return s, e


def online(ls, c):
    tmin = ls.min(axis=0)
    tmax = ls.max(axis=0)
    if tmin[0] <= c[0] and tmax[0] >= c[0] and tmin[1] <= c[1] and tmax[1] >= c[1]:
        #print ls[1,0]
        if ls[1, 0]-ls[0, 0] == 0:
            if c[0] == ls[1, 0]:
                return True
            else:
                return False
        else:
            y = int((c[0]-ls[0, 0])*(ls[1, 1]-ls[0, 1])/(ls[1, 0]-ls[0, 0])+ls[0, 1])
        #print y
        if y == c[1]:
            return True
    return False


def getPanel(tri, x, y):
    #print tri[0],tri[1],tri[2]
    p = Plane(Point3D(tri[0]), Point3D(tri[1]), Point3D(tri[2]))
    b = Point3D([x, y, 0])
    return N(p.distance(b))
