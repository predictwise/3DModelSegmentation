__author__ = 'wlw'
# -*- coding: utf-8 -*-
from shapely.geometry import Polygon
import numpy as np
from sklearn.decomposition import PCA
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import vtk
#from citypca import *
from shapely import *
from shapely.geometry import *

#将Polygon几何polys转换为indexfaceset表示，如果是二维多边形，则默认高度为0，dh为可设置的高度偏移
def get2DPoly(polys , dh = 0):
        print "show polygons"
        tp = []
        idx = []
        faces = []
        h = 0
        k = 0
        for p in polys:
            for c in p:
                print c
                if len(c)==3:
                    faces.append([c[0] , c[1] , c[2]])
                else:
                    faces.append([c[0] , c[1] , h])
                idx.append(k)
                k+=1
            idx.append(-1)
            h+=dh
        return faces , idx

#可视化Polygon几何ps
def vispoly(ps):
    faces , idx = get2DPoly(ps)
    #faces, idx = [[0.0, 0.0, 0], [0.0, 1.0, 0], [1.0, 1.0, 0], [1.0, 2.0, 0], [2.0, 2.0, 0], [2, 1, 0], [3.0, 1.0, 0], [3.0, 0.0, 0]], [0,7,6,5,4,3,2,1, -1]
    print faces, idx
    visu(getPoly(faces , idx))

#对Polygon pi和pj进行PCA分析
def analysis(pi , pj):
    print 'shape analysis'
    #print pj,pj
    p = []
    p.extend(pi)
    p.extend(pj)
    pca=PCA(n_components=2)
    pca.fit(p)
    pcai = PCA(n_components=2)
    pcai.fit(pi)
    pcaj = PCA(n_components=2)
    pcaj.fit(pj)
    pi2 = pca.transform(pi)
    pj2 = pca.transform(pj)
    pio = pcai.transform(pi)
    pjo = pcaj.transform(pj)
    ppi = Polygon(pi2)
    ppj = Polygon(pj2)
    ppio = Polygon(pio)
    ppjo = Polygon(pjo)
    print ppi.area, ppj.area,ppio.area,ppjo.area
    vispoly([pi,pj])
    vispoly([pi2,pj2,pio,pjo])
    #vispoly([pio,pjo])

#判断点c0与c1是否为同一个点，误差为dx，dy
def isSame(c0,c1):
    dx = 0.01
    dy = 0.01
    #print 'isSame:',c0,c1
    if abs(c0[0]-c1[0])<dx and abs(c0[1]-c1[1])<dy:
        return True
    else:
        return False

#判断c0与c1是否是es中的一个边
def isEdge(c0,c1,es):
    #print 'isEdge:',c0,c1,es
    for e in es:
        if isSame(c0,e[0]) and isSame(c1,e[1]):
            return True
        if isSame(c1 , e[0]) and isSame(c0,e[1]):
            return True
    return False

#判断边e1与e2是否相连
def isConnected(e1,e2):
    if isSame(e1[0],e2[0]) and isSame(e1[-1],e2[-1]):
        return e1
    if isSame(e1[-1],e2[0]) and isSame(e1[0],e2[-1]):
        return e1
    res = []

    if isSame(e1[0],e2[0]):
        res.extend(e1[::-1])
        res.extend(e2[1:])
        return res
    elif isSame(e1[0],e2[-1]):
        res.extend(e2)
        res.extend(e1[1:])
        return res
    elif isSame(e1[-1],e2[0]):
        res.extend(e1)
        res.extend(e2[1:])
        return res
    elif isSame(e1[-1],e2[-1]):
        res.extend(e1[:-1])
        res.extend(e2[::-1])
        return res
    return res

#判断c是否是边几何es中某个边上的点
def getEdgeNd(c, es):
    res = []
    for e in es:
        if isSame(c, e[0]):
            res.append(e[1])
        if isSame(c, e[1]):
            res.append(e[0])
    #print 'ge:',res
    return res

#
def getRouts(cs, ce, es):
    tes = []
    tes.append(es)
    res = []
    res.append(cs)
    fg = True
    while fg:
        fg = False
        cc = res[-1]
        if not isSame(cc,ce):
            return

def poly2Edge(ps):
    res = []
    for i in range(len(ps)-1):
        e = [ps[i],ps[(i+1)%len(ps)]]
        res.append(e)
    return res

def edge2Poly(es):
    ps = []
    tes = []
    tes.extend(es)

    fl = True
    while len(tes)>0 and fl:
        fl = False
        l = len(tes)
        for i in range(l):
            for j in range(l):
                if i!=j:
                    ti = tes[i]
                    tj = tes[j]
                    tij = isConnected(ti,tj)
                    #print 'ti,ti,tij:',ti,tj,tij
                    #print len(tes)
                    if len(tij)>0:
                        tes.remove(ti)
                        tes.remove(tj)
                        tes.append(tij)
                        fl = True
                        break
            if fl:
                break
    # print 'e2pin:',tes
    return tes


def getLS(p , e):
    p0 = Point((e[0][0] , e[0][1]))
    p1 = Point((e[1][0] , e[1][1]))
    if p0.distance(p)==0 or p1.distance(p)==0:
        return False
    line = LineString([(e[0][0] , e[0][1]) , (e[1][0] , e[1][1])])
    if line.distance(p)==0:
        return True

def find(c,es):
    for i in range(len(es)):
        for j in range(len(es[i])):
            if isSame(es[i][j],c):
                return i,j
    return -1,-1

def divide(cx,es,rcx):
    res = []
    l = len(cx)-1
    print cx,l
    print rcx
    for i in range(l):
        c0 = cx[i]
        c1 = cx[(i+1)%l]
        if not isEdge(c0 , c1 , rcx):
            x0 , y0 = find(c0 , es)
            x1 , y1 = find(c1 , es)
            if x0==x1:
                for a in range(y0,y1):
                    cx.insert(i+a,)


class layer:

    cs = []
    maxd = 0.3

    def __init__(self, c):
        self.bot = c[2]
        self.top = c[2]
        self.d = 0
        self.cs = []
        self.cs.append(c)

    def add(self, c):
        if abs(c[2]-self.bot)>self.maxd or abs(c[2]-self.top)>self.maxd:
            return False
        self.cs.append(c)
        if c[2]>self.top:
            self.top = c[2]
        elif c[2]<self.bot:
            self.bot = c[2]
        self.d = self.top-self.bot
        return True
    def contain(self,c):
        if c[2]<self.top+self.maxd and c[2]>self.bot-self.maxd:
            return True
        return False


    def addES(self,ps):

        self.es = []
        self.ces = []
        cx = self.getCVX()
        cxp = poly2Edge(cx)
        for p in ps:
            #print 'p:',p
            for ei in range(len(p)):
                if self.contain(p[ei]) and self.contain(p[(ei+1)%len(p)]):
                    e = [p[ei],p[(ei+1)%len(p)]]
                    #print 'e:',e
                    for c in cx:
                        ci = getEdgeNd(c,[e])
                        #print 'add:',c,ci
                        if len(ci)>0 and not isEdge(e[0],e[1],cxp):
                            self.es.append(e)
                            break
                        elif isEdge(e[0],e[1],cxp):
                            self.ces.append(e)
                            break
        #print 'cxp:',cxp
        #print 'es:',self.es
        #print 'e2p:',edge2Poly(self.es)



    def getCVX(self):
        tcs = []
        for t in self.cs:
            tcs.append([t[0],t[1],self.bot])
        mp = MultiPoint(tcs)
        cx = mp.convex_hull
        ps = []
        for m in mp:
            #print 'cvx:',m
            if not cx.contains(m):
                ps.append(m)
        #print ps
        res = []
        if cx.type=='Polygon':
            for c in cx.exterior.coords:
                res.append([c[0],c[1],self.bot])
        for p in ps:
            l = len(res)
            for i in range(l):
                if getLS(p, [res[i],res[(i+1)%l]]):
                    res.insert(i+1,[p.x,p.y,self.bot])
                    break
        #print 'cx:',res
        return res


    def getBCVX(self):

        cx = self.getCVX()
        fg = True
        ps = edge2Poly(self.es)
        l = len(cx)
        print 'ces', self.ces
        print 'ps', ps
        cxp = poly2Edge(cx)
        #divide(cx,ps,self.ces)
        fl = True
        print 'getBCVX:'
        res = []
        while fl and len(cx)>0:
            fl = False
            nres = []
            #nres.append(cx[0])
            i = 0
            while i<l:
                ci = cx[i]
                nres.append(cx[i])
                cix,ciy = find(ci,ps)
                if cix == -1:
                    i += 1
                    continue

                cj = cx[(i+1)%l]
                #print 'ci,cj',ci,cj
                cjx,cjy = find(cj,ps)
                if cix==cjx:
                    if ciy > cjy:
                        #print ps[cix][cjy+1:ciy]
                        nres.extend(ps[cix][cjy+1:ciy])
                    elif ciy < cjy:
                        #print cx[ciy:cjy]
                        nres.extend(ps[cix][ciy+1:cjy])
                i += 1
            res.append(nres)
        #vispoly(res[0])
        #print 'res:',res[0][:-1]
        if len(res)>0:
            return res[0][:-1]
        else:
            return res


                    #return







        #return
    def getPoly(self):
        tcs = []
        for t in self.cs:
            cc = Point(t[0],t[1])
            tcs.append(cc)
        pcs = []
        ti = 0
        pi = 0
        pcs.append(tcs[ti])
        del tcs[ti]
        while len(tcs)>0:
            mi = 0
            m = 10000
            for i in range(len(tcs)):
                d = pcs[pi].distance(tcs[i])
                if d<m:
                    m = d
                    mi = i

            pcs.append(tcs[mi])
            del tcs[mi]
            pi+=1

        #print pcs
        res = []
        for p in pcs:
            print p.coords[:]
            x,y = p.coords[0][0],p.coords[0][1]
            res.append([x,y,self.bot])

        return res

#计算由二维坐标点集合ps围成的凸多边形convex hull的面积大小
def getCVXarea(ps):
    #print 'getCVXarea',ps
    tcs = []
    for t in ps:
        tcs.append([t[0],t[1],0])
    mp = MultiPoint(tcs)
    cx = mp.convex_hull
    #print cx.area
    return cx.area

def slide(ps):

    ls = []
    cs = []
    for p in ps:
        cs.extend(p)

    cs.sort(key=lambda x:x[2])
    #print cs
    d = 0
    ls.append(layer(cs[0]))
    for c in cs:
        if not ls[d].add(c):
            d+=1
            ls.append(layer(c))
    pss = []
    for l in ls:
        print len(l.cs),l.d
        l.addES(ps)
        #l.getBCVX()
        r = l.getBCVX()
        if len(r)>0:
            print 'r:',r
            pss.append(r)

    vispoly(pss)


if __name__ == '__main__':
    print 'start'
    ps = [[0,0,0],[10,0,0],[10,10,0],[1,1,1],[5,50,0]]
    ps2 = [[0,0,0],[2,0,0],[2,1,0],[1,1,0],[1,2,0],[0,2,0]]
    ps22 = [[0,0,0],[0,2,0],[1,2,0],[1,1,0],[2,1,0],[2,0,0]]
    ps23 = [[0,0,0],[3,0,0],[3,1,0],[2,1,0],[2,2,0],[1,2,0],[1,1,0],[0,1,0],[0,0,0]]
    ps3 = [[[0,0,0],[1,0,0],[1,1,0],[0,1,0]],[[2,0,0],[3,0,0],[3,2,0],[2,2,0]]]
    ps4 = []
    #slide(ps3)
    #slide([ps23])
    getCVXarea(ps)


