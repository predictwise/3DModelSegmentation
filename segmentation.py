__author__ = 'wlw'
# coding=utf-8

from numpy import *
import time, os, StringIO, collada
import matplotlib.pyplot as plt
from collada import *
import numpy as np
import gravity, translation, scaling, myVisu, rotation, kmeanspp, extractingCells, kmeans
from mpl_toolkits.mplot3d import Axes3D


def readZipModel(kmzfile, name):
    print 'name: ', name
    # 解压kmz文件。r表示是读取zip文件;w是创建一个zip文件
    unzipFile = zipfile.ZipFile(kmzfile, 'r')
    # 解压之后的文件列表
    fileLists = unzipFile.namelist()

    # 后缀
    postfix = ['dae']
    mesh = None

    for each_file in fileLists:
        if each_file[-3:] in postfix[0]:
            dae_data = unzipFile.read(each_file)
            mesh = Collada(StringIO.StringIO(dae_data))
            # 此种方法解压后有文件出现，不好
            # daeFile = unzipFile.extract(unzipFile.getinfo(each_file))
            # mesh = Collada(daeFile)

    unzipFile.close()

    # 一个大的模型由多个几何模型构成
    print 'geometries num: ', len(mesh.geometries)


    boundprimType = ''
    allTriPolygones = []
    allLinelists = []
    for boundgeom in mesh.scene.objects('geometry'):
        # 存放每一个几何模型的面
        polygones = []
        linelists = []
        # 每个几何模型又由多个更低级的原语(三角形,线段,多边形)构成
        for boundprim in boundgeom.primitives():
            # print 'boundprim: ', boundprim
            # 分别算三角形和线
            if isinstance(boundprim, collada.triangleset.BoundTriangleSet):
                # type: <class 'collada.triangleset.TriangleSet'>
                boundprimType = 'boundtriangleset'
                boundprimList = list(boundprim)

                for i in range(len(boundprimList)):
                    # 得到每一个boundprimitive(三角形)的顶点坐标
                    # 形如: [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]
                    # 并加入到polygones中
                    polygones.append(boundprim.vertex[boundprim.vertex_index][i])

            elif isinstance(boundprim, collada.lineset.BoundLineSet):
                # type: <class 'collada.lineset.LineSet'>
                boundprimType = 'boundlineset'
                boundprimList = list(boundprim)

                for i in range(len(boundprimList)):
                    # 得到每一个boundprimitive(线)的顶点坐标
                    # 形如: [[x1,y1,z1],[x2,y2,z2]]
                    # 并加入到linelists中
                    linelists.append(boundprim.vertex[boundprim.vertex_index][i])

        allTriPolygones.append(polygones)
        #allLinelists.append(linelists)

    return allTriPolygones
    # return allPolygones, allLinelists


# 平移、缩放规一化
def normalize(allTriPolygones):
    # 平移变换, 将模型重心作为空间原点
    mp, transed_tripoints = translation.translate(allTriPolygones)
    '''
    # 旋转变换
    rotated_points = rotation.rotate(transed_points)
    '''
    # 缩放变换, 返回最终预处理好的模型
    # final_points是一个二维的nx3数组，每一行代表三角形的一个顶点
    final_tripoints = scaling.scale(mp, transed_tripoints)

    return final_tripoints


def main(kmzdir):
    kmzfiles = os.listdir(kmzdir)
    for kmzfile in kmzfiles:
        name = kmzfile[:-4]
        kmzfile = os.path.join(kmzdir, kmzfile)

        allTriPolygones = readZipModel(kmzfile, name)
        final_tripoints = normalize(allTriPolygones)

        '''
        # 可视化规一化后的整个三维模型
        actor = myVisu.get3Dpolyactor(final_tripoints)
        myVisu.displayModel(actor)
        '''

        # 只包含三角形, 用K-means++
        dataSet = gravity.getGravitySet(final_tripoints)
        dataSet = np.mat(dataSet)
        k = 5
        '''
        # 只包含三角形, 用K-means
        centroids, clusterAssment = kmeans.kmeans(dataSet, k)
        # kmeanspp.showCluster(dataSet, k, centroids, clusterAssment)
        '''

        # 用K-means++
        centroids = kmeanspp.kpp(dataSet, k)
        centroids, clusterAssment = kmeanspp.kmeans(dataSet, k, centroids)
        kmeanspp.showCluster(dataSet, k, centroids, clusterAssment)

        actor0, actor1, actor2, actor3, actor4 = extractingCells.extractCells(final_tripoints, clusterAssment)
        myVisu.displayModel2(actor0, actor1, actor2, actor3, actor4)


if __name__ == '__main__':
    start = time.clock()
    kmzdir = '/home/wlw/wh3d/test/'
    main(kmzdir)

    total = time.clock() - start
    print 'time: ', total


