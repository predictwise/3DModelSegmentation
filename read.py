__author__ = 'wlw'
# coding=utf-8

import collada
import numpy
import sys, time
import os
import zipfile
from collada import *
import StringIO
import pylab
import matplotlib
from sympy import *
import matplotlib.pyplot as plt


def readfile(f, name, start):
    print 'name: ', name
    # print f
    ext = os.path.splitext(f)[1]
    # print ext
    if ext == '.kmz':
        readzip(f, name, start)
    elif ext == '.zip':
        readzip(f, name, start)


def readzip(f, name, start):

    # 这里的第二个参数用r表示是读取zip文件，w是创建一个zip文件
    z = zipfile.ZipFile(f, 'r')
    for f in z.namelist():
        # 分离文件名与扩展名；返回(fname,fextension)元组
        ext = os.path.splitext(f)[1]
        if ext == '.dae':
            dae_data = z.read(f)
            mesh = Collada(StringIO.StringIO(dae_data))
            print 'geometries num: ', len(mesh.geometries)
            geom = mesh.geometries[0]
            triset = geom.primitives[0]
            trilist = list(triset)
            #print len(trilist)
            # print trilist[0]
            #print triset.vertex[triset.vertex_index][0]
            #print triset.normal[triset.normal_index][0]

            #for n in mesh.scene.nodes:
                #print 'node:',n,n.children
            #getGroundRect(mesh)
            #getNodeGeo(mesh.scene.nodes)
            readgeos(mesh, name, start)

    z.close()


def readgeos(mesh, name, start):
    boundgeoms = list(mesh.scene.objects('geometry'))
    allgeo = None
    flag = True

    alltri = []

    for geo in boundgeoms:
        #print geo
        boundprims = list(geo.primitives())
        for prim in boundprims:
            if len(prim) > 0:
                tris = (list(prim))
                #print prim
                #print tris[0].vertices
                #print tris[0].indices
                #alltri.extend(tris)
                for tri in tris:
                    # 三角形的顶点
                    tv = tri.vertices
                    #print 'tv: ', tv

                    #print 'tv',tv
                    #print 'mtv',tv[tv.argmin(axis=0)][0]
                    #print tri
                    alltri.append(tv)
                    if flag:
                        allgeo = tv
                        flag = False
                    else:
                        # 将tv加入到allgeo中，axis=0是沿着列计算；axis=1是沿着行计算
                        # 若不指定axis，那么最终的结果是一个一维数组
                        # allgeo的类型：<type 'numpy.ndarray'>
                        # 存放三角形的顶点
                        allgeo = numpy.append(allgeo, tv, axis=0)

                # print 'alltri: ', alltri
    '''
    print 'type: ', type(allgeo)
    print 'len(alltri): ', len(alltri)
    print 'alltri[0:9]: ', alltri[0:9]
    print 'len(allgeo): ', len(allgeo)
    print 'allgeo[0:9]: ', allgeo[0:9]
    print 'shape: ', allgeo.shape
    print 'allgeo.min(axis=0): ', allgeo.min(axis=0)
    print 'allgeo.max(axis=0): ', allgeo.max(axis=0)
    '''
    # (nn, bins) = numpy.histogram(allgeo, bins=50, normed=True)
    #print nn,bins
    #pylab.plot(.5*(bins[1:]+bins[:-1]), nn)
    #pylab.show()
    # getHist(allgeo)
    # print len(alltri)
    getTriHist(alltri, allgeo, name, start)


def online(ls, c):
    tm = ls.min(axis=0)
    tx = ls.max(axis=0)
    #print tm,tx,c
    if tm[0] <= c[0] and tx[0] >= c[0] and tm[1] <= c[1] and tx[1] >= c[1]:
        #print ls[1,0]
        if ls[1,0]-ls[0,0]==0:
            if c[0]==ls[1,0]:
                return True
            else:
                return False
        else:
            y = int((c[0]-ls[0,0])*(ls[1,1]-ls[0,1])/(ls[1,0]-ls[0,0])+ls[0,1])
        #print y
        if y == c[1]:
            return True
    return False
    pass


def touch(tri, x, y0, y1):
    ls1 = tri[0:2]
    ls2 = tri[1:]
    ls3 = tri[0:3:2]
    f = 0
    s = -1
    e = -1
    #print 'touch:',ls1,ls2,ls3,x,y0,y1
    for y in range(y0,y1+1):
        c = numpy.array([x,y])
        if online(ls1,c) or online(ls2,c) or online(ls3,c):
            if f==0:
                s = y
                f = 1
            elif f==1:
                e = y
                pass
            if f==2:
                e = y
            if f==1:
                pass
        elif f==1:
            f=2

    if f==1:
        e = y1
    elif f==2:
        pass
    else:
        e = s+1
    #print s,e
    return s, e

    pass


def getPanel(tri,x,y):
    #print tri[0],tri[1],tri[2]
    p = Plane(Point3D(tri[0]), Point3D(tri[1]), Point3D(tri[2]))
    b = Point3D([x,y,0])
    return N(p.distance(b))
    pass


def getZvalue(tri):
    res = []
    if tri.shape == (3, 3):
        tm = tri.min(axis=0)
        tx = tri.max(axis=0)
        # print 'tri2:', tri

        # touch(tri,None)
        for i in range(int(tm[0]), int(tx[0])):
            s, e = touch(tri, i, int(tm[1]), int(tx[1]))
            for j in range(s, e):
                res.append([i, j, getPanel(tri, i, j)])

    elif tri.shape == (2, 3):
        # print 'line'
        pass

    return res


def getTriHist(alltri, allgeo, name, start, resx=200, resy=200):
    minxyz = allgeo.min(axis=0)
    maxxyz = allgeo.max(axis=0)
    dxyz = maxxyz-minxyz
    # print 'dxyz: ', dxyz
    dv = numpy.array([resx+1, resy+1, 255])
    res = numpy.zeros((resx+1, resy+1))

    for tri in alltri:
        # print 'tri1: ', tri
        # //：取整除 - 返回商的整数部分
        t = (tri-minxyz)*dv//dxyz
        zv = getZvalue(t)
        # print 'zv: ', zv
        for z in zv:
            if res[z[0], z[1]] < z[2]:
                res[z[0], z[1]] = z[2]

    # matplotlib.image.imsave('nametri.png', res)
    plt.imshow(res)
    plt.savefig('/home/wlw/wh3d/histogram/'+name+'.png')
    total = time.clock() - start
    print 'time: ', total


def getHist(allgeo, resx=1000, resy=1000):
    # 每一列的最小值
    minxyz = allgeo.min(axis=0)
    # 每一列的最大值
    maxxyz = allgeo.max(axis=0)
    #print maxxyz-minxyz
    dx = maxxyz[0]-minxyz[0]
    dy = maxxyz[1]-minxyz[1]
    dz = maxxyz[2]-minxyz[2]
    res = numpy.zeros((resx+1, resy+1))
    for r in allgeo:
        x = int(resx*(r[0]-minxyz[0])/dx)
        y = int(resy*(r[1]-minxyz[1])/dy)
        z = int(255*(r[2]-minxyz[2])/dz)
        # print z
        if z > res[x, y]:
            res[x, y] = z
    print 'res: ', res
    matplotlib.image.imsave('name.png', res)
    #plt.imshow(res)
    #plt.savefig('name1.png')


def printnode(node):
    print 'print node', type(node)
    if type(node) is scene.GeometryNode:
        triset = node.geometry.primitives[0]
        trilist = list(triset)
        print 'trilist:', triset[0]
        #print


def getNodeGeo(nodes):
    for n in nodes:
        if type(n) is scene.GeometryNode:
            #print 'geometry',n
            pass
        elif type(n) is scene.Node:
            #print 'node',n.children
            if len(n.transforms)>0 and len(n.children)>0:
                print n.transforms[0].matrix
                trs = n.transforms[0]
                print n
                print 'no:', n.children[0]
                printnode(n.children[0])
                n.save()
                print 'nt:', n.children[0]
                printnode(n.children[0])
            if len(n.children) > 0:
                #for n in node.children:
                getNodeGeo(n.children)

        elif type(n) is scene.NodeNode:
            if len(n.node.transforms)>0:
                print n.node.transforms[0].matrix
                trs = n.node.transforms[0]
                print 'no:', n.node
                n.node.save()
                print 'nt:', n.node
            if len(n.node.children) > 0:
                getNodeGeo(n.node.children)
        else:
            print type(n)


    pass


def getGroundRect(mesh):
    k = 0
    rect = [0, 0, 0, 0]
    for geom in mesh.geometries:
        for triset in geom.primitives:
            #k+=1
            #print triset
            if len(triset) > 0:
                for tri in triset:
                    k += 1
                    #print tri
                    break

    print 'k:', k


# 读取zip文件
def readpath(path):
    lists = os.listdir(path)
    for fn in lists:
        start = time.clock()
        name = fn[:-4]
        f = os.path.join(path, fn)
        readfile(f, name, start)



def main():
    models = '/home/wlw/wh3d/testing/'
    readpath(models)

if __name__ == '__main__':
    main()