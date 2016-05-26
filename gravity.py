__author__ = 'wlw'
# coding=utf-8


# 获取每一个三角面片的重心
def getGravitySet(points):
    '''
    # 去除重复的顶点，只保留一个
    res = {point.tostring(): point for point in points}
    duped_points = res.values()
    #print 'duped_points: ', duped_points
    '''

    gravitySet = []
    for i in xrange(len(points)/3):
        # 第i个三角形
        a_pt = points[i*3]
        b_pt = points[i*3+1]
        c_pt = points[i*3+2]

        # 第i个三角形的重心
        g = (a_pt+b_pt+c_pt) / 3.0
        gravitySet.append(g)

    return gravitySet

    # return duped_points

# 获取每一条线的中心
def getMiddleSet(points):
    middleSet = []
    for i in xrange(len(points)/2):
        # 第i条线
        a_pt = points[i*2]
        b_pt = points[i*2+1]

        # 第i条线的中心
        m = (a_pt+b_pt) / 2.0
        middleSet.append(m)

    return middleSet