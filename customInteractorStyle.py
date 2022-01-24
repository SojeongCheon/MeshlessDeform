import vtk
import numpy as np
import utils
from deformation import Deformation

class pointPickingInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self):
        self.AddObserver('RightButtonPressEvent', self.right_button_press_event)
        self.AddObserver('RightButtonReleaseEvent', self.right_button_release_event)
        
        self.start_pt = None
        self.end_pt = None
        self.pt_id = -1
        self.picked_actor = None
        
        self.deformation_method = None
        
    def right_button_press_event(self, obj, event):
        pos2D = self.GetInteractor().GetEventPosition()
        
        picker = vtk.vtkPointPicker()
        picker.Pick(pos2D[0], pos2D[1], 0, self.GetDefaultRenderer())
                
        self.picked_actor = picker.GetActor()
        
        if self.picked_actor == None:
            self.OnRightButtonDown()
            
        else:
            if self.deformation_method == None :
                input_points = self.picked_actor.GetMapper().GetInput().GetPoints()
                self.deformation_method = Deformation(input_points)
                print("#### copy points of the polydata done!")
            
            self.start_pt = picker.GetPickPosition()
            self.pt_id = picker.GetPointId()
                    
            # print("start pos3D :", self.start_pt)
            # print("picked point id :", self.pt_id)
            
            sphere = vtk.vtkSphereSource()
            sphere.SetCenter(self.start_pt)
            sphere.Update()
            
            sphere_actor = utils.MakeActor(sphere.GetOutput())
            sphere_actor.GetProperty().SetColor(1,0.8,0)
            self.GetDefaultRenderer().AddActor(sphere_actor)
            self.GetDefaultRenderer().GetRenderWindow().Render()        
        return 
    
    def right_button_release_event(self, obj, event):
        pos2D = self.GetInteractor().GetEventPosition()
        
        picker = vtk.vtkPointPicker()
        picker.Pick(pos2D[0], pos2D[1], 0, self.GetDefaultRenderer())
                
        if self.picked_actor == None:
            self.OnRightButtonUp()
            
        else:
            self.end_pt = picker.GetPickPosition()
            # print("end pos3D :", self.end_pt)

            ################### here deformation@!
            delta = np.array(self.end_pt) - np.array(self.start_pt)
            self.deformation_method.quadratic_deform(delta, self.pt_id)
        
            self.picked_actor = None
            self.pt_id = -1
        return


# class propPickingInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
#     def __init__(self):
#         self.AddObserver('RightButtonPressEvent', self.right_button_press_event)
#         self.AddObserver('RightButtonReleaseEvent', self.right_button_release_event)
        
#         self.start_pt = None
#         self.end_pt = None
#         self.picked_actor = None
        
        
#     def right_button_press_event(self, obj, event):
#         print('************* down')
#         pos2D = self.GetInteractor().GetEventPosition()
        
#         picker = vtk.vtkPropPicker()
#         picker.Pick(pos2D[0], pos2D[1], 0, self.GetDefaultRenderer())
#         self.start_pt = picker.GetPickPosition()
                
#         print("pos3D :", self.start_pt)
        
#         self.picked_actor = picker.GetActor()
#         if self.picked_actor == None:
#             print('miss ><')
            
#             self.OnRightButtonDown()
            
#         else:
#             sphere = vtk.vtkSphereSource()
#             sphere.SetCenter(self.start_pt)
#             sphere.Update()
            
#             sphere_actor = utils.MakeActor(sphere.GetOutput())
#             sphere_actor.GetProperty().SetColor(1,0.8,0)
#             self.GetDefaultRenderer().AddActor(sphere_actor)
#             self.GetDefaultRenderer().GetRenderWindow().Render()        
#         return 
    
#     def right_button_release_event(self, obj, event):
#         print('************* up')
#         pos2D = self.GetInteractor().GetEventPosition()
        
#         picker = vtk.vtkPropPicker()
#         picker.Pick(pos2D[0], pos2D[1], 0, self.GetDefaultRenderer())
#         self.end_pt = picker.GetPickPosition()
#         print("pos3D :", self.end_pt)
        
#         if self.picked_actor == None:
#             self.OnRightButtonUp()
#         else:
#             self.picked_actor = None
#         return
    