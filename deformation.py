from re import A
import numpy as np
import scipy.linalg
import vtk
from vtk.util import numpy_support

h = 0.2
mass = 1.0

class Deformation():
    def __init__(self, points, h=0.2, m=1.0):
        self.h = h
        self.mass = mass
        self.damping = 0.05
        self.alpha = 1.0
        self.beta = 0.9
        self.w_force = 1.0 / 10.0
        
        # points
        self.cur_points = numpy_support.vtk_to_numpy(points.GetData()).copy()
        self.cur_points = np.expand_dims(self.cur_points, 2)
        
        self.next_points = self.cur_points.copy()
        self.goal_points = self.cur_points.copy()
        
        self.num_points = self.cur_points.shape[0]
        
        # initialization
        self.force = np.zeros_like(self.cur_points, dtype=float)
        self.velocity = np.zeros_like(self.cur_points, dtype=float)
        self.p = np.zeros_like(self.cur_points, dtype=float)
        
        self.X0cm = self.cur_points * self.mass
        self.X0cm = np.sum(self.X0cm, 0)
        self.X0cm /= (mass * self.num_points)
        
        self.q = self.cur_points - self.X0cm
        
        self.Aqq = np.zeros((3,3))
        for idx in range(self.num_points):
            qq = self.q[idx]
            self.Aqq += self.mass * qq * qq.transpose()
        self.Aqq = np.linalg.inv(self.Aqq)
        
        self.q_hat = np.zeros((self.num_points, 9, 1))
        for idx in range(self.num_points):
            qq = self.q[idx]
            self.q_hat[idx] = np.array([ qq[0], qq[1], qq[2],
                                        qq[0]*qq[0], qq[1]*qq[1], qq[2]*qq[2],
                                        qq[0]*qq[1], qq[1]*qq[2], qq[2]*qq[0]])
            
        self.Aqq_hat = np.zeros((9,9))
        for idx in range(self.num_points):
            qq_hat = self.q_hat[idx]
            self.Aqq_hat += self.mass * qq_hat * qq_hat.transpose()
        
    def quadratic_deform(self, delta, pt_id):
        self.force = np.zeros_like(self.cur_points, dtype=float)
        self.velocity = np.zeros_like(self.cur_points, dtype=float)
        
        # update force, velocity
        k = self.mass * self.num_points * self.h
        delta =  np.expand_dims(np.array(delta), 1)
        self.force[pt_id] = k * delta
        # self.velocity[pt_id] = np.zeros(3,1)
        
        # compute Xcm
        Xcm = np.zeros((3,1))
        for idx in range(self.num_points):
            Xcm += np.array(self.cur_points[idx])*self.mass
        Xcm /= mass * self.num_points
        
        # compute p vector
        self.p = self.cur_points - Xcm
        
        # compute Apq
        Apq = np.zeros((3,3))
        for idx in range(self.num_points):
            pp = self.p[idx]
            qq = self.q[idx]
            Apq += self.mass * pp * qq.transpose()
            
        # compute rotation matrix R
        S = Apq.transpose() * Apq
        R = Apq * scipy.linalg.sqrtm(S)
        
        for idx in range(self.num_points):
            qq = self.q[idx]
            self.goal_points[idx] = np.matmul(R, qq) + Xcm           
    
        for idx in range(self.num_points):
            self.velocity[idx] = (1 - self.damping) * self.velocity[idx] + self.alpha * (self.goal_points[idx] - self.cur_points[idx]) / self.h + self.h * self.force[idx] / self.mass
            self.next_points[idx] = self.cur_points[idx] + self.h * self.velocity[idx]
            
        return self.next_points
        