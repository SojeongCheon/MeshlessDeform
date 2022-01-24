import os, glob
import vtk

def LoadMesh(path):
    ext = os.path.basename(path).split('.')[-1]

    if   ext == 'stl' : reader = vtk.vtkSTLReader()
    elif ext == 'obj' : reader = vtk.vtkOBJReader()
    elif ext == 'ply' : reader = vtk.vtkPLYReader()
    else: raise Exception('Check File')
    
    reader.SetFileName(path)
    reader.Update()
    
    return reader.GetOutput()

def MakeActor(poly):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly)
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    return actor
