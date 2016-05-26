__author__ = 'wlw'
# coding=utf-8

from numpy import *
import time, os, StringIO, collada
import matplotlib.pyplot as plt
from collada import *
import numpy as np
import gravity, translation, scaling, myVisu, rotation
from mpl_toolkits.mplot3d import Axes3D


# calculate Euclidean distance
def euclDistance(vector1, vector2):
    return sqrt(sum(power(vector2 - vector1, 2)))


# init centroids with random samples
def initCentroids(dataSet, k, n=0):
    numSamples, dim = dataSet.shape
    print 'dim: ', dim
    centroids = zeros((k, dim))
    index = int(random.uniform(0, numSamples))
    centroids[n, :] = dataSet[index, :]
    n += 1
    return centroids, n


def kpp(dataSet, k):
    # n为确定下来的种子点的个数
    centroids, n = initCentroids(dataSet, k)
    numSamples = dataSet.shape[0]
    print 'numsamples: ', numSamples

    for t in xrange(1, k):
        dist = []
        summ = 0
        for i in xrange(numSamples):
            minDist = 100000.0
            for j in range(n):
                distance = euclDistance(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist = distance
                    dist.append(minDist)
            summ += minDist

        rdom = random.random()*summ
        for j in xrange(numSamples):
            rdom -= dist[j]
            if rdom <= 0:
                centroids[t, :] = dataSet[j, :]
                n += 1
                break

    return centroids

# k-means cluster
def kmeans(dataSet, k, centroids):
    numSamples = dataSet.shape[0]
    # first column stores which cluster this sample belongs to,
    # second column stores the error between this sample and its centroid
    clusterAssment = mat(zeros((numSamples, 2)))
    clusterChanged = True

    # step 1: init centroids
    # centroids = initCentroids(dataSet, k)

    while clusterChanged:
        clusterChanged = False
        # for each sample
        for i in xrange(numSamples):
            minDist = 100000.0
            minIndex = 0
            # for each centroid
            # step 2: find the centroid who is closest
            for j in range(k):
                distance = euclDistance(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist = distance
                    # 样本点和下标为j的种子点属于一类
                    minIndex = j

            # step 3: update its cluster
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
                clusterAssment[i, :] = minIndex, minDist**2

        # step 4: update centroids
        for j in range(k):
            # numpy函数返回非零元素的下标
            # 返回值为元组， 两个值分别为两个维度， 包含了相应维度上非零元素的目录值
            # e.g.: nonzero(a) 返回值为 (array([0, 1]), array([0, 0]))
            # 因为矩阵a只有两个非零值， 在第0行、第0列，和第1行、第0列。所以结果元组中，第一个行维度数据为（0,1） 元组第二个列维度都为（0,0）
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
            # print 'pointsInCluster: ', pointsInCluster
            # 求种子点的均值
            centroids[j, :] = mean(pointsInCluster, axis=0)

    return centroids, clusterAssment


# show your cluster only available with 3-D data
def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr'] # 例子
    # mark = ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', '.', '.', '.', '.', '+', '+', '+', '+']  # k=8
    # mark = ['r', 'b', 'g', 'k', 'c', 'm', 'y', '.', '.', '.', '.', '+', '+', '+']  # k=7
    # mark = ['r', 'b', 'g', 'k', 'c', 'y',  '.', '.', '.', '+', '+', '+']  # k=6
    mark = ['r', 'b', 'g', 'k', 'y',  'o', 'o', 'o', '+', '+']  # k=5
    # mark = ['r', 'g', 'k', 'y', '.', '.', '+', '+']  # k=4
    # draw all samples
    for i in xrange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        # plt.plot(dataSet[i, 0], dataSet[i, 1], dataSet[i, 2], mark[markIndex])
        ax.scatter(dataSet[i, 0], dataSet[i, 1], dataSet[i, 2], c=mark[markIndex], marker=mark[markIndex+5])

    # mark2 = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  # 例子
    # mark2 = ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'r', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']  # k=8
    # mark2 = ['r', 'b', 'g', 'k', 'c', 'm', 'y', 'D', 'D', 'D', 'D', 'D', 'D', 'D']  # k=7
    # mark2 = ['r', 'b', 'g', 'k', 'c', 'y', 'D', 'D', 'D', 'D', 'D', 'D']  # k=6
    mark2 = ['r', 'b', 'g', 'k', 'y', 'D', 'D', 'D', 'D', 'D']  # k=5
    # mark2 = ['r', 'g', 'k', 'y', 'D', 'D', 'D', 'D']  # k=4
    # draw the centroids
    for i in range(k):
        # plt.plot(centroids[i, 0], centroids[i, 1], centroids[i, 2], mark[i], markersize=12)
        ax.scatter(centroids[i, 0], centroids[i, 1], centroids[i, 2], c=mark2[i], marker=mark2[i+5])

    # 坐标轴
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')

    plt.show()
    # plt.savefig()


