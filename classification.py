__author__ = 'wlw'
# coding=utf-8

import zipfile, os, time, collada, shutil
from collada import *
import numpy as np
import myVisu, translation, scaling, rotation, histogram, eigvalue
import sqlite3, math, cvtNparr, StringIO


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
    allPolygones = []

    for boundgeom in mesh.scene.objects('geometry'):
        # 存放每一个几何模型的面
        polygones = []

        # 每个几何模型又由多个更低级的原语(三角形,线段,多边形)构成
        for boundprim in boundgeom.primitives():
            # print 'boundprim: ', boundprim

            '''
            # 三角形和线都算
            boundprimList = list(boundprim)
            # print 'len: ', len(boundprimList)

            for i in range(len(boundprimList)):
                # 得到每一个boundprimitive(比如三角形, 或者线)的顶点坐标
                # 形如: [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]
                # 并加入到polygones中
                polygones.append(boundprim.vertex[boundprim.vertex_index][i])
            '''

            # 只算三角形
            if isinstance(boundprim, collada.triangleset.BoundTriangleSet):
                # type: <class 'collada.triangleset.TriangleSet'>
                boundprimType = 'boundtriangleset'
                boundprimList = list(boundprim)
                for i in range(len(boundprimList)):
                    # 得到每一个boundprimitive(比如三角形, 或者线)的顶点坐标
                    # 形如: [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]
                    # 并加入到polygones中
                    polygones.append(boundprim.vertex[boundprim.vertex_index][i])

            elif isinstance(boundprim, collada.lineset.BoundLineSet):
                # type: <class 'collada.lineset.LineSet'>
                boundprimType = 'boundlineset'
                continue



        '''
        if boundprimType == 'boundtriangleset':
            # print pcagen(polygones, 0.99)
            # polygones是一个三维数组
            # print 'polygones: ', polygones
            actor = myVisu.get3Dpolyactor(polygones)
            myVisu.displayPolygones(actor)
            break
        '''

        allPolygones.append(polygones)

    normalize(allPolygones, name)


# 旋转规一化
def normalize(allPolygones, name):
    # 平移变换, 将模型重心作为空间原点
    mp, transed_points = translation.translate(allPolygones)
    # 旋转变换
    rotated_points = rotation.rotate(transed_points)
    # 缩放变换, 返回最终预处理好的模型
    # final_points是一个二维的nx3数组，每一行代表三角形的一个顶点
    final_points = scaling.scale(mp, rotated_points)
    # 原本final_points是list类型，转换为<type 'numpy.ndarray'>
    final_points = np.array(final_points)


    #extractEigvect(final_points, name)
    #eigvectflat(final_points, name)


    # 测试生成二维投影直方图
    # histogram.getHist(final_points)
    allTris = []
    for i in range(len(final_points)/3):
        allTris.append(final_points[i*3:i*3+3])
    #allTris = np.array(allTris)
    # print 'type(allTris): ', type(allTris)
    histogram.getTriHist(allTris, final_points, name, 200, 200)




def eigvectflat(final_points, name):
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, cvtNparr.adapt_array)
    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", cvtNparr.convert_array)

    conn = sqlite3.connect("/home/wlw/oliverProjects/3DClassification/classification.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    maxs_xoy = eigvalue.extractXOY(final_points)
    maxs_xoz = eigvalue.extractXOZ(final_points)
    tmp = np.vstack((maxs_xoy, maxs_xoz))
    maxs_yoz = eigvalue.extractYOZ(final_points)
    eigvects = np.vstack((tmp, maxs_yoz))
    print 'eigvects: ', eigvects

    cur.execute("insert into model values (?,?,?)", (name, eigvects, 'flat'))
    conn.commit()
    conn.close()



# 提取特征向量
def extractEigvect(final_points, name):
    # myVisu.visu2DXOY(final_points)
    # myVisu.visu2DXOZ(final_points)
    # myVisu.visu2DYOZ(final_points)

    maxs_xoy = eigvalue.extractXOY(final_points)
    maxs_xoz = eigvalue.extractXOZ(final_points)
    tmp = np.vstack((maxs_xoy, maxs_xoz))
    maxs_yoz = eigvalue.extractYOZ(final_points)
    eigvects = np.vstack((tmp, maxs_yoz))

    classify(eigvects, name)



    #actorX_Y, actorX_Z, actorY_Z = myVisu.get3Dpolyactor(allPolygones)
    #myVisu.displayPolygones(actorX_Y, actorX_Z, actorY_Z)

    '''
    # 测试投影到YOZ平面
    actorY_Z = myVisu.get3Dpolyactor(allPolygones)
    myVisu.displayPolygones(actorY_Z)
    '''

    '''
    # 测试，可视化旋转规一化后的三维模型
    actor = myVisu.get3Dpolyactor2(final_points)
    myVisu.displayModel(actor)
    '''

    '''
    # 测试生成二维投影直方图
    # histogram.getHist(final_points)
    allTris = []
    for i in range(len(final_points)/3):
        allTris.append(final_points[i*3:i*3+3])
    #allTris = np.array(allTris)
    print 'type(allTris): ', type(allTris)
    histogram.getTriHist(allTris, final_points)
    '''


def classify(eigvects, name):
    print 'eigvects: ', eigvects
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, cvtNparr.adapt_array)
    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", cvtNparr.convert_array)

    conn = sqlite3.connect("/home/wlw/oliverProjects/3DClassification/classification.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    cur.execute("select eigvects, id from model where type='flat'")
    lists = cur.fetchall()
    for lis in lists:
        # lis是一个tuple
        #print 'lis[0]: ', lis[0]
        #print type(lis[0])

        res = lis[0] - eigvects
        summ = 0
        for r in res:
            d = math.sqrt(sum(math.pow(value, 2) for value in r))
            summ += d

        similarity = summ / 3.0
        print '%s\'s  similarity with %s is %f ' % (lis[1], name, similarity)

    conn.close()


def main(kmzdir):
    kmzfiles = os.listdir(kmzdir)
    for kmzfile in kmzfiles:
        name = kmzfile[:-4]
        # kmzfile = kmzdir + kmzfile
        kmzfile = os.path.join(kmzdir, kmzfile)
        readZipModel(kmzfile, name)


if __name__ == '__main__':
    start = time.clock()
    #train_kmzdir = '/home/wlw/wh3d/training/'
    #main(train_kmzdir)

    test_kmzdir = '/home/wlw/wh3d/testing/'
    main(test_kmzdir)

    total = time.clock() - start
    print 'time: ', total