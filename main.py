import vtk
import os, glob
import argparse

from customInteractorStyle import pointPickingInteractorStyle
import utils

ren = vtk.vtkRenderer()
ren.SetBackground(90./255., 20./255., 255./255.)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(1000,1000)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renWin)
style = pointPickingInteractorStyle()
interactor.SetInteractorStyle(style)
style.SetDefaultRenderer(ren)

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='resources/Stanford_Bunny.stl')
args = parser.parse_args()

if __name__ == "__main__":
    input = utils.LoadMesh(args.input)
    input_actor = utils.MakeActor(input)
    ren.AddActor(input_actor)
    
    print("************* ", input.GetPoint(0))
    
    interactor.Initialize()
    renWin.Render()
    interactor.Start()
