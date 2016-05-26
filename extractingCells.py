# coding=utf-8
__author__ = 'wlw'

import vtk


def extractCells(final_tripoints, clusterAssment):
    polys0 = []
    polys1 = []
    polys2 = []
    polys3 = []
    polys4 = []
    numSamples = clusterAssment.shape[0]
    for i in xrange(numSamples):
        cluster_index = int(clusterAssment[i, 0])
        if cluster_index == 0:
            poly0 = []
            poly0.append(final_tripoints[i*3])
            poly0.append(final_tripoints[i*3+1])
            poly0.append(final_tripoints[i*3+2])
            polys0.append(poly0)
        elif cluster_index == 1:
            poly1 = []
            poly1.append(final_tripoints[i*3])
            poly1.append(final_tripoints[i*3+1])
            poly1.append(final_tripoints[i*3+2])
            polys1.append(poly1)
        elif cluster_index == 2:
            poly2 = []
            poly2.append(final_tripoints[i*3])
            poly2.append(final_tripoints[i*3+1])
            poly2.append(final_tripoints[i*3+2])
            polys2.append(poly2)
        elif cluster_index == 3:
            poly3 = []
            poly3.append(final_tripoints[i*3])
            poly3.append(final_tripoints[i*3+1])
            poly3.append(final_tripoints[i*3+2])
            polys3.append(poly3)
        elif cluster_index == 4:
            poly4 = []
            poly4.append(final_tripoints[i*3])
            poly4.append(final_tripoints[i*3+1])
            poly4.append(final_tripoints[i*3+2])
            polys4.append(poly4)

    points0 = vtk.vtkPoints()
    print 'len(tris): ', len(polys0)
    for p in polys0:
        points0.InsertNextPoint(p[0])
        points0.InsertNextPoint(p[1])
        points0.InsertNextPoint(p[2])

    tris0 = vtk.vtkCellArray()
    for i in range(len(polys0)):
        tri = vtk.vtkTriangle()
        tri.GetPointIds().SetId(0, 3*i)
        tri.GetPointIds().SetId(1, 3*i+1)
        tri.GetPointIds().SetId(2, 3*i+2)
        tris0.InsertNextCell(tri)

    trisPolyData0 = vtk.vtkPolyData()
    trisPolyData0.SetPoints(points0)
    trisPolyData0.SetPolys(tris0)

    mapper0 = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper0.SetInput(trisPolyData0)
    else:
        mapper0.SetInputData(trisPolyData0)

    actor0 = vtk.vtkActor()
    actor0.SetMapper(mapper0)


    points1 = vtk.vtkPoints()
    print 'len(tris): ', len(polys1)
    for p in polys1:
        points1.InsertNextPoint(p[0])
        points1.InsertNextPoint(p[1])
        points1.InsertNextPoint(p[2])

    tris1 = vtk.vtkCellArray()
    for i in range(len(polys1)):
        tri = vtk.vtkTriangle()
        tri.GetPointIds().SetId(0, 3*i)
        tri.GetPointIds().SetId(1, 3*i+1)
        tri.GetPointIds().SetId(2, 3*i+2)
        tris1.InsertNextCell(tri)

    trisPolyData1 = vtk.vtkPolyData()
    trisPolyData1.SetPoints(points1)
    trisPolyData1.SetPolys(tris1)

    mapper1 = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper1.SetInput(trisPolyData1)
    else:
        mapper1.SetInputData(trisPolyData1)

    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)


    points2 = vtk.vtkPoints()
    print 'len(tris): ', len(polys2)
    for p in polys2:
        points2.InsertNextPoint(p[0])
        points2.InsertNextPoint(p[1])
        points2.InsertNextPoint(p[2])

    tris2 = vtk.vtkCellArray()
    for i in range(len(polys2)):
        tri = vtk.vtkTriangle()
        tri.GetPointIds().SetId(0, 3*i)
        tri.GetPointIds().SetId(1, 3*i+1)
        tri.GetPointIds().SetId(2, 3*i+2)
        tris2.InsertNextCell(tri)

    trisPolyData2 = vtk.vtkPolyData()
    trisPolyData2.SetPoints(points2)
    trisPolyData2.SetPolys(tris2)

    mapper2 = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper2.SetInput(trisPolyData2)
    else:
        mapper2.SetInputData(trisPolyData2)

    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)


    points3 = vtk.vtkPoints()
    print 'len(tris): ', len(polys3)
    for p in polys3:
        points3.InsertNextPoint(p[0])
        points3.InsertNextPoint(p[1])
        points3.InsertNextPoint(p[2])

    tris3 = vtk.vtkCellArray()
    for i in range(len(polys3)):
        tri = vtk.vtkTriangle()
        tri.GetPointIds().SetId(0, 3*i)
        tri.GetPointIds().SetId(1, 3*i+1)
        tri.GetPointIds().SetId(2, 3*i+2)
        tris3.InsertNextCell(tri)

    trisPolyData3 = vtk.vtkPolyData()
    trisPolyData3.SetPoints(points3)
    trisPolyData3.SetPolys(tris3)

    mapper3 = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper3.SetInput(trisPolyData3)
    else:
        mapper3.SetInputData(trisPolyData3)

    actor3 = vtk.vtkActor()
    actor3.SetMapper(mapper3)


    points4 = vtk.vtkPoints()
    print 'len(tris): ', len(polys4)
    for p in polys4:
        points4.InsertNextPoint(p[0])
        points4.InsertNextPoint(p[1])
        points4.InsertNextPoint(p[2])

    tris4 = vtk.vtkCellArray()
    for i in range(len(polys4)):
        tri = vtk.vtkTriangle()
        tri.GetPointIds().SetId(0, 3*i)
        tri.GetPointIds().SetId(1, 3*i+1)
        tri.GetPointIds().SetId(2, 3*i+2)
        tris4.InsertNextCell(tri)

    trisPolyData4 = vtk.vtkPolyData()
    trisPolyData4.SetPoints(points4)
    trisPolyData4.SetPolys(tris4)

    mapper4 = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper4.SetInput(trisPolyData4)
    else:
        mapper4.SetInputData(trisPolyData4)

    actor4 = vtk.vtkActor()
    actor4.SetMapper(mapper4)

    return actor0, actor1, actor2, actor3, actor4



