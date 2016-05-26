__author__ = 'wlw'

import vtk

def getpsactor(ps):

    # create source
    src = vtk.vtkPointSource()
    src.SetCenter(0, 0, 0)
    src.SetNumberOfPoints(50)
    src.SetRadius(5)
    src.Update()
    # ps = [[1,1,1],[2,2,2]]
    # print src.GetOutput()
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()
    for p in ps:
        # Create the topology of the point (a vertex)
        if len(p) == 2:
            p = [p[0], p[1], 0]
        id = points.InsertNextPoint(p)
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(id)

    # Create a polydata object
    point = vtk.vtkPolyData()

    # Set the points and vertices we created as the geometry and topology of the polydata
    point.SetPoints(points)
    point.SetVerts(vertices)
    # mapper
    # mapper = vtk.vtkPolyDataMapper()
    # Visualize
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(point)
    else:
        mapper.SetInputData(point)

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().SetPointSize(2)
    # assign actor to the renderer
    return actor


def getlsactor(ls):
    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()

    for l in ls:
        points.InsertNextPoint(l[0])
        points.InsertNextPoint(l[1])

    # Create a cell array to store the lines in and add the lines to it
    lines = vtk.vtkCellArray()

    for i in range(len(ls)):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 2*i)
        line.GetPointIds().SetId(1, 2*i+1)
        lines.InsertNextCell(line)

    # Create a polydata to store everything in
    linesPolyData = vtk.vtkPolyData()

    # Add the points to the dataset
    linesPolyData.SetPoints(points)

    # Add the lines to the dataset
    linesPolyData.SetLines(lines)

    # Setup actor and mapper
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(linesPolyData)
    else:
        mapper.SetInputData(linesPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


def get3Dpolyactor(pl):
    poly = []
    for i in range(len(pl)/3):
        # print i,pl[3*i:3*i+3]
        poly.append(pl[3*i:3*i+3])
    # print poly
    return getpolyactor(poly)


def getpolyactor(poly, h=0):

    points = vtk.vtkPoints()
    for p in poly:
        print 'getpolyactor', p
        if len(p) == 2:
            p = [p[0], p[1], h]

        points.InsertNextPoint(p)

    # Create the polygon
    polygon = vtk.vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(len(poly)-1)
    for i in range(len(poly)-1):
        polygon.GetPointIds().SetId(i, i)
    # polygon.GetPointIds().SetId(0, 0)

    # Add the polygon to a list of polygons
    polygons = vtk.vtkCellArray()
    polygons.InsertNextCell(polygon)

    # Create a PolyData
    polygonPolyData = vtk.vtkPolyData()
    polygonPolyData.SetPoints(points)
    polygonPolyData.SetPolys(polygons)

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(polygonPolyData)
    else:
        mapper.SetInputData(polygonPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def visups(ps):
    showact([getpsactor(ps)])

def showact(actors):

    cols = [(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)]

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    cn = 0
    for a in actors:

        # color the actor
        a.GetProperty().SetColor(cols[cn%len(cols)])  # (R,G,B)
        renderer.AddActor(a)
        cn += 1
    # renderer.AddActor(actor2)

    renderWindow.Render()
    renderWindowInteractor.Start()
