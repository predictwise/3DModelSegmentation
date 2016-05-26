__author__ = 'zcq'
# coding=utf-8
import time, os, StringIO, zipfile, collada
from collada import *
import numpy as np


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

            #getGroundRect(mesh)
            getNodeGeo(mesh.scene.nodes)

    unzipFile.close()

    # 一个大的模型由多个几何模型构成
    print 'geometries num: ', len(mesh.geometries)


def getNodeGeo(nodes):
    print 'nodes: ', nodes
    for n in nodes:
        # print 'n: ', n  # <Node transforms=0, children=9>
        # [<Node transforms=1, children=1>, <Node transforms=1, children=1>]
        # 或者 [<CameraNode camera=Camera-camera>]之类
        # print 'children: ', n.children
        # scene.GeometryNode对应于<instance_geometry>标签
        if type(n) is scene.GeometryNode:
            print 'GeometryNode: ', n
        # scene.Node对应于<node>标签
        elif type(n) is scene.Node:
            # 既有MatrixTransform，又有instance_geometry
            if len(n.transforms) > 0 and len(n.children) > 0:
                # print 'n.transforms', n.transforms  # [<MatrixTransform>]
                print 'matrix: ', n.transforms[0].matrix
                # print 'n: ', n  # <Node transforms=1, children=6>
                print 'n.children: ', n.children  # [<GeometryNode geometry=ID3>, <GeometryNode geometry=ID16>]
                # <instance_geometry>标签, 即child。通过url来映射到GeometryNode，即<geometry>标签
                print 'no:', n.children[0]
                '''
                for child in n.children:
                    printnode(child)
                '''
                printnode(n.children[0])
                #n.save()
                #print 'nt:', n.children[0]
                #printnode(n.children[0])

            if len(n.children) > 0:
                #for n in node.children:
                getNodeGeo(n.children)

        #　代表一个已经被实例化的node，对应于<instance_node>标签
        elif type(n) is scene.NodeNode:
            if len(n.node.transforms) > 0:
                print n.node.transforms[0].matrix
                trs = n.node.transforms[0]
                print 'no:', n.node
                n.node.save()
                print 'nt:', n.node
            if len(n.node.children) > 0:
                getNodeGeo(n.node.children)
        else:
            print 'other: ', type(n)



def printnode(node):
    print 'print node', type(node)
    lis = []
    if type(node) is scene.GeometryNode:
        # print 'node.geometry.primitives: ', node.geometry.primitives  # [<TriangleSet length=77>]可能有线或有三角形，或者二者都有
        print 'len: ', len(node.geometry.primitives)
        triset = node.geometry.primitives[0]   # 不单单取0
        # print 'triset: ', triset  # <TriangleSet length=77>
        trilist = list(triset)
        # 由一个个三角形构成 [<Triangle ([9.75 617.99932861 61.43856049], [9.75 528.49841309 12.75], [2.27373703e-13 6.17999329e+02 6.14385605e+01], "Material2")>]
        print 'trilist: ', trilist
        print 'len(trilist): ', len(trilist)
        print 'triset[0]:', triset[0]
        print 'type(triset[0]): ', type(triset[0])  # <class 'collada.triangleset.Triangle'>
        lis.append(triset[0])
        # lis = np.array(lis)
        print 'lis: ', lis
        print 'type(l): ', type(lis)
        for li in lis:
            triv = li.vertices
            print 'triv: ', triv
            print 'type(triv): ', type(triv)





def main(kmzdir):
    kmzfiles = os.listdir(kmzdir)
    for kmzfile in kmzfiles:
        name = kmzfile[:-4]
        kmzfile = os.path.join(kmzdir, kmzfile)
        readZipModel(kmzfile, name)

if __name__ == '__main__':
    start = time.clock()
    #train_kmzdir = '/home/wlw/wh3d/training/'
    #main(train_kmzdir)

    # test_kmzdir = '/home/wlw/wh3d/testing/'
    test_kmzdir = '/home/wlw/wh3d/test/'
    main(test_kmzdir)

    total = time.clock() - start
    print 'time: ', total