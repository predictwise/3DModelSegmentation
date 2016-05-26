# coding=utf-8
__author__ = 'wlw'

import vtk
from vtk.util.colors import tomato
import pylab as pl
import numpy as np


# 用于可视化整个模型
def get3Dpolyactor(final_tripoints):
    polys = []
    for i in xrange(len(final_tripoints)/3):
        poly = []
        poly.append(final_tripoints[3*i])
        poly.append(final_tripoints[3*i+1])
        poly.append(final_tripoints[3*i+2])
        polys.append(poly)
    # print 'polys: ', polys

    points = vtk.vtkPoints()
    print 'len(tris): ', len(polys)
    for p in polys:
        points.InsertNextPoint(p[0])
        points.InsertNextPoint(p[1])
        points.InsertNextPoint(p[2])

    tris = vtk.vtkCellArray()
    for i in range(len(polys)):
        tri = vtk.vtkTriangle()
        tri.GetPointIds().SetId(0, 3*i)
        tri.GetPointIds().SetId(1, 3*i+1)
        tri.GetPointIds().SetId(2, 3*i+2)
        tris.InsertNextCell(tri)

    trisPolyData = vtk.vtkPolyData()
    trisPolyData.SetPoints(points)
    trisPolyData.SetPolys(tris)

    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(trisPolyData)
    else:
        mapper.SetInputData(trisPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


# 可视化整个模型
def displayModel(actor):
    actor.GetProperty().SetColor(tomato)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    # renderer.SetViewport(0, 0, 0.5, 0.5)
    renderer.SetBackground(0.1, 0.2, 0.4)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800)

    # 添加鼠标交互
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)

    # 初始化交互器 并开始执行事件循环
    iren.Initialize()
    iren.Start()


# K-means++聚类后五个分割部分的可视化
def displayModel2(actor0, actor1, actor2, actor3, actor4):
    actor0.GetProperty().SetColor(tomato)
    actor1.GetProperty().SetColor(tomato)
    actor2.GetProperty().SetColor(tomato)
    actor3.GetProperty().SetColor(tomato)
    actor4.GetProperty().SetColor(tomato)

    renderer0 = vtk.vtkRenderer()
    renderer0.AddActor(actor0)
    renderer0.SetViewport(0, 0.5, 0.3, 1)
    renderer0.SetBackground(0.1, 0.2, 0.4)

    renderer1 = vtk.vtkRenderer()
    renderer1.AddActor(actor1)
    renderer1.SetViewport(0.3, 0.5, 0.6, 1)
    renderer1.SetBackground(0.1, 0.2, 0.4)

    renderer2 = vtk.vtkRenderer()
    renderer2.AddActor(actor2)
    renderer2.SetViewport(0, 0, 0.3, 0.5)
    renderer2.SetBackground(0.1, 0.2, 0.4)

    renderer3 = vtk.vtkRenderer()
    renderer3.AddActor(actor3)
    renderer3.SetViewport(0.3, 0, 0.6, 0.5)
    renderer3.SetBackground(0.1, 0.2, 0.4)

    renderer4 = vtk.vtkRenderer()
    renderer4.AddActor(actor4)
    renderer4.SetViewport(0.6, 0, 0.9, 0.5)
    renderer4.SetBackground(0.1, 0.2, 0.4)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer0)
    renderWindow.AddRenderer(renderer1)
    renderWindow.AddRenderer(renderer2)
    renderWindow.AddRenderer(renderer3)
    renderWindow.AddRenderer(renderer4)
    renderWindow.SetSize(1500, 800)

    # 添加鼠标交互
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)

    # 初始化交互器 并开始执行事件循环
    iren.Initialize()
    iren.Start()



