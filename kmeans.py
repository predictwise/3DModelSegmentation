__author__ = 'wlw'
# coding=utf-8

from numpy import *
import time
import matplotlib.pyplot as plt


# calculate Euclidean distance
def euclDistance(vector1, vector2):
    return sqrt(sum(power(vector2 - vector1, 2)))


# init centroids with random samples
def initCentroids(dataSet, k):
    numSamples, dim = dataSet.shape
    centroids = zeros((k, dim))
    for i in range(k):
        # 在0～numSamples之间随机生成一个数
        index = int(random.uniform(0, numSamples))
        centroids[i, :] = dataSet[index, :]
    return centroids


# k-means cluster
def kmeans(dataSet, k):
    numSamples = dataSet.shape[0]
    print 'numsamples: ', numSamples
    # first column stores which cluster this sample belongs to,
    # second column stores the error between this sample and its centroid
    clusterAssment = mat(zeros((numSamples, 2)))
    clusterChanged = True

    # step 1: init centroids
    centroids = initCentroids(dataSet, k)

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
            centroids[j, :] = mean(pointsInCluster, axis=0)

    print 'Congratulations, cluster complete!'
    return centroids, clusterAssment


# show your cluster only available with 2-D data
def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print "Sorry! I can not draw because the dimension of your data is not 2!"
        return 1

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print "Sorry! Your k is too large! please contact Zouxy"
        return 1

    # draw all samples
    for i in xrange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)

    plt.show()

'''
if __name__ == '__main__':
    # step 1: load data
    print "step 1: load data..."
    dataSet = []
    fileIn = open('/home/wlw/testSet.txt')
    for line in fileIn.readlines():
        lineArr = line.strip().split(',')
        #print 'type(lineArr[0]): ', type(lineArr[0])
        dataSet.append([float(lineArr[0]), float(lineArr[1])])

    # step 2: clustering...
    print "step 2: clustering..."
    dataSet = mat(dataSet)
    print 'dataSet: ', dataSet
    k = 4
    centroids, clusterAssment = kmeans(dataSet, k)

    # step 3: show the result
    print "step 3: show the result..."
    showCluster(dataSet, k, centroids, clusterAssment)
'''

