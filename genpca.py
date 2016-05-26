# -*- coding: utf-8 -*-
__author__ = 'wlw'

import ConfigParser
lcf = ConfigParser.ConfigParser()
lcf.read('../conf.ini')

import sys
#print lcf.get('s2','abs_path')
sys.path.append('./util')

#import CityGMLFile as cf
import visu
import os
import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
import pcashapely
# import outputx3d as out

# pts是二维数据, 计算由pts围成的二维区域的面积
def PolyArea2D(pts):
    # hstack: 横着合并数组
    lines = np.hstack([pts, np.roll(pts, -1, axis=0)])
    area = 0.5*abs(sum(x1*y2-x2*y1 for x1, y1, x2, y2 in lines))
    return area


# polys：[[[0, 0, 0], [1, 1, 1], [0.5, 0.5, 3], [0, 1, 0]]]
def get2DInfo(polys):
    r2d = []
    # 最小z坐标值
    r = -1000000
    # 最大z坐标值
    g = 1000000
    for poly in polys:
        for p in poly:
            # 将x和y坐标值加入r2d
            r2d.append([p[0], p[1]])
            if p[2] > r:  # ？
                r = p[2]
            if p[2] < g:  # ？
                g = p[2]
    return r2d, r, g
    pass

# polys：[[[0, 0, 0], [1, 1, 1], [0.5, 0.5, 3], [0, 1, 0]]]
def getlod2(polys):
    # ps: [[0, 0], [1, 1], [0.5, 0.5], [0, 1]]
    # r: 3
    # g: 0
    ps, r, g = get2DInfo(polys)
    cv = ConvexHull(ps)
    hp = cv.vertices
    print cv
    l = len(hp)
    res = []
    pg = []
    pr = []
    for i in range(len(hp)):
        x0,y0 = ps[hp[i]]
        x1,y1 = ps[hp[(i+1)%l]]
        rp = [[x0,y0,g],[x1,y1,g],[x1,y1,r],[x0,y0,r]]
        res.append(rp)
        pg.append([x0,y0,g])
        pr.append([x0,y0,r])
    res.append(pg)
    res.append(pr)
    #print res
    return res
    pass

def merge(gps):
    ps = []
    for p in gps:
        ps.extend(p)
    return [getlod2(ps)]
    pass

def distp(p1,p2):
    res = 10000
    for c1 in p1:
        for c2 in p2:
            r = abs(c1[0]-c2[0])+abs(c1[1]-c2[1])+abs(c1[2]-c2[2])
            if r <res:
                res = r
    return res
    pass

def distps(ps1,ps2):
    #print 'ps:',ps1,ps2
    res = 10000
    for p1 in ps1:
        for p2 in ps2:
            r = distp(p1,p2)
            if r<res:
                res=r
    return res
    pass

def getlod1(bds, limt=10):
    group = []

    for polys in bds:
        ag = []
        lg = []
        for g in group:
            fg = False
            for ps in g:
                if distps(polys,ps)<limt:
                    #print 'merge:',ag,g
                    ag.extend(g)
                    ag.append(polys)
                    ag = merge(ag)
                    fg = True

            if not fg:
                lg.append(g)
        if len(ag) == 0:
            lg.append([polys])
        else:
            lg.append(ag)
        group = lg
        #print 'len group:',len(group)

        #print 'group:',group,ag,lg

    print 'len group:',len(group)
    res = []
    for g in group:
        print len(g)
        gps = []
        for ps in g:
            gps.extend(ps)
        res.extend(getlod2(ps))

    return res

# 默认方差百分比=99%
def pcagen(polys, dv=0.99):
    l = len(polys)
    print 'l: ', l

    if l > 3000 or l <= 0:
        return []
        pass

    # 主成分方差百分比
    pcas = np.zeros((l, l), dtype=float)
    # 面积
    area = np.zeros((l, l), dtype=float)
    for i in range(l):
        for j in range(i, l):
            if i == j:
                # 对数组的操作
                pcas[i, j] = 0
                area[i, j] = 0
                continue
            # x轴的数据?
            pi = polys[i]
            print 'pi: ', pi

            # y轴的数据?
            pj = polys[j]
            print 'pj: ', pj

            p = []
            # extend()方法只接受一个list作为参数，并将该参数的每个元素都添加到原有的列表中
            p.extend(pi)
            p.extend(pj)
            # 设置将3D->2D数据
            pca = PCA(n_components=2)
            # fit(p)，表示用数据p来训练PCA模型
            pca.fit(p)
            # 将数据pi（三维数据）转换成降维后的数据pi2（二维数据）
            pi2 = pca.transform(pi)
            pj2 = pca.transform(pj)
            # analysis(pi,pj)
            # 存放什么面积？
            print 'PolyArea2D(pi2): ', PolyArea2D(pi2)
            print 'PolyArea2D(pj2): ', PolyArea2D(pj2)
            area[i, j] = PolyArea2D(pi2)-PolyArea2D(pj2)
            # 返回所保留的2个主成分各自的方差百分比之和
            pcas[i, j] = pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]
            print 'pcas[i, j]: ', pcas[i, j]

    rem = []
    deles = []
    while pcas.max() > dv:
        if len(rem) > len(polys)-5:  # 为什么要减5？
            break
        # pcas.argmax()：得到一个数组中最大元素的位置，e.g. np.array([[10,50,30],[60,20,40]])最大元素的位置为3
        # pcas.shape返回一个元组（行数,列数）
        # p.unravel_index(pcas.argmax(), pcas.shape)，以元组的形式返回最大元素的位置, 对应上面的例子为(1,0)
        i, j = np.unravel_index(pcas.argmax(), pcas.shape)

        pi = polys[i]
        pj = polys[j]
        # print pi
        # print pj
        p = []
        p.extend(pi)
        p.extend(pj)
        pca = PCA(n_components=2)
        pca.fit(p)
        pi2 = pca.transform(pi)
        pj2 = pca.transform(pj)
        p2 = pca.transform(p)
        # analysis(pi,pj) 计算出进过pca变换后pi,pj及其点集的凸多边形的面积
        api = PolyArea2D(pi2)
        apj = PolyArea2D(pj2)
        ap2 = pcashapely.getCVXarea(p2)
        # print 'pca area:',ap2,api,apj
        if ap2 > max(api, apj)*1.3:  # 如果凸多边形面积ap2大于最大面积的1.3倍，则不进行删除
            # print 'if pca area:',ap2,api,apj
            pcas[i, j] = 0
            continue
        if area[i, j] > 0:
            # print 'pcas:',pcas[i,:].max(), pcas[j,:].max()
            if not j in rem:
                rem.append(j)
                deles.append((j, i, apj, api, ap2, pcas[j, i]))
                for k in range(l):
                    pcas[k, j] = 0
                    pcas[j, k] = 0

        else:
            if not i in rem:
                rem.append(i)
                deles.append((i, j, api, apj, ap2, pcas[i, j]))
                for k in range(l):
                    pcas[k, i] = 0
                    pcas[i, k] = 0
        pcas[i, j] = 0
        pcas[j, i] = 0

        #print pcas.max()
        #print pcas
    #print len(rem)
    #print rem
    newpolys = []
        #print 'rem:',rem

    for i in range(len(polys)):
        if not i in rem:
            newpolys.append(polys[i])

    return newpolys

'''
def run():
    #file = '../s4_PCAgen/hcity.gml'
    #getCityObjects(file)
    zdir = '/home/wlw/K40/data/citygml/'
    odir = '/home/wlw/Proj/visu3d/data/nsf3d/s1/x3d/'
    zfs = os.listdir(zdir)
    ns = {}
    nc = {}
    for zfn in zfs:
        # 单个gml压缩文件
        zf = zdir+zfn
        #print zf
        # 解压缩，cons？ conc？
        cons, conc = cf.readzipcity(zf)
        polys = cf.getVPoly(conc)
        pcapolylist = cf.getPCAPolyList(conc)

        # print 'vps:',len(polys)
        # print 'pca:',len(pcapolylist)
        opath = odir+zfn
        ox3df = opath[:-4]
        gpolys = []
        k = 0
        n = len(pcapolylist)
        for pp in pcapolylist:

            gps = pcagen(pp)
            gpolys.extend(gps)
            print 'bl:', k, n, len(pp), len(gps)
            k += 1
            #print gps
            #break
        #vv.visupoly(polys)
        #vv.visupoly(gpolys)
        gf = ox3df+'_'+str(len(gpolys))+'.x3d'
        out.outx3d(gpolys, gf)
        of = ox3df+'_'+str(len(polys))+'.x3d'
        out.outx3d(polys, of)
        for tag in cons:
            if tag in ns:
                ns[tag] += cons[tag]
                nc[tag].extend(conc[tag])
            else:
                ns[tag] = cons[tag]
                nc[tag] = conc[tag]
        #for type in ns:
            #print type,nc[type],ns[type]
    #print ns
    #print nc
    for n in ns:
        print n
    print ''
    building_type = '{http://www.opengis.net/citygml/building/1.0}Building'
    #showObjects(type,nc)
    land_type = '{http://www.opengis.net/citygml/landuse/1.0}LandUse'
    ##road_type = '{http://www.opengis.net/citygml/transportation/1.0}Road'
    #cf.showObjects(road_type,nc)
'''

if __name__ == '__main__':
    #run()
    polys = [[[0, 0, 0], [1, 1, 1], [0.5, 0.5, 3], [0, 1, 0]]]
    # print getlod2(polys)
    print pcagen(polys, 0.99)
