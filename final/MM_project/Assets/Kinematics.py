#!/usr/bin/env python
"""Kinematics.py
Handles the inverse kinematics and jacobians for the robot

@author Gerry and Carter
"""

import numpy as np

LINK_LENGTHS = [0, 3, 3, 3]  #changed this not sure if it is correct
BASE_OFFSET = [0, 0, 1]
Q_INITIAL = [0, 0, 0, 0, 90, 0, 0]

def sind(th):
    return np.sin(np.deg2rad(th))
def cosd(th):
    return np.cos(np.deg2rad(th))
def wrap(th):
    return np.rad2deg(np.arctan2(sind(th), cosd(th)))
def R(th): 
    return np.array([[cosd(th), -sind(th)],
                     [sind(th), cosd(th)]])

"""ik - Inverse Kinematics of the 4DoF robot arm
Args:
    x:      (x, y, z) position of the camera
    theta:  normal vector of the camera projected onto the x-y plane
    phi:    angle between normal vector and z-axis
    L:      4-vector representing lengths of the 4 links (link 0 is usually 0)
    Q0:     angles of the 4 joints at rest configuration, where all zeros would be the arm pointing
            straight out in the +x direction, ie (sum(L), 0, 0)
"""
def ik_arm(x, theta, phi, L=LINK_LENGTHS, Q0=Q_INITIAL[3:]):
    theta = wrap(theta + 180)
    # convenience setup
    x = np.reshape(x, (3, 1))
    ct, st = cosd(theta), sind(theta)
    Rt = np.array([[ct, -st, 0],
                   [st, ct, 0],
                   [0, 0, 1]])
    Rp = R(phi)
    # rotate x into the plane defined by theta
    xplane = Rt.T @ x
    xplane = xplane[[0,2]]

    # subtract transforms of first and last links
    L3 = Rp @ np.reshape([0, L[3]], (2, 1))
    x3 = xplane - L3
    x1 = np.reshape([L[0], 0], (2, 1))
    x13 = (x3 - x1).flatten()   # vector from joint 1 to joint 3
    
    # use law of cosines and law of sines to figure out poses of links 1 and 2
    alpha = np.arccos(- (np.dot(x13, x13) - L[1]**2 - L[2]**2) / (2*L[1]*L[2]))
    beta = np.arcsin(np.sin(alpha) * L[2] / np.linalg.norm(x13))
    x13angle = np.arctan2(x13[1], x13[0])
    alpha = np.rad2deg(alpha)   # interior angle between links 1 and 2
    beta = np.rad2deg(beta)     # angle between x13 and link 1
    x13angle = np.rad2deg(x13angle) # angle to horizontal

    # convert and return
    q = np.array([theta, x13angle-beta, 180-alpha, phi-(90+x13angle-alpha-beta)])
    # print(q)
    return q

"""ik - Inverse Kinematics of the robot
Args:
    x:      (x, y, z) position of the camera
    theta:  normal vector of the camera projected onto the x-y plane
    phi:    angle between normal vector and z-axis
    L:      4-vector representing lengths of the 4 links (link 0 is usually 0)
    BO:     transform from the base center to the arm base
    Q0:     angles of the 4 joints at rest configuration, where all zeros would be the arm pointing
            straight out in the +x direction
"""
def ik(x, theta, phi, L=LINK_LENGTHS, BO=BASE_OFFSET, Q0=Q_INITIAL):
    # separate base and arm.  Choose configuration that minimizes base movement
    v = np.array([cosd(theta), sind(theta), 0])
    if np.linalg.norm(x) > 0.001:
        xbase = x - v * np.dot(v, x)
        xbase[2] = 0
    else:
        xbase = np.array([0., 0., 0])
    
    # subtract out base transform and do ik
    xarm = x - xbase - BO
    qarm = ik_arm(xarm, theta, phi, L, Q0)

    return np.array([xbase[0], xbase[1], 0, *qarm])

# def jacobian(q, L=LINK_LENGTHS, Q0=Q_INITIAL):
#     """ Calculate manipulator Jacobian.
#         Takes numpy array of joint angles, in radians.
#     """        
    
#     alpha = theta_b + q[0]
#     beta = theta_b + q[0] + q[1]
#     gamma = theta_b + q[0] + q[1] + q[2]
#     delta = theta_b + q[0] + q[1] + q[2] + q[3]

#     cosines = np.array([np.cos(alpha), np.cos(beta), np.cos(gamma), np.cos(delta)])
#     sines = np.array([np.sin(alpha), np.sin(beta), np.sin(gamma), np.sin(delta)])
#     Ls = np.array([self.L1, self.L2, self.L3, self.L4]).T

#     Jacobian = np.zeros((3, 7))
#     Jacobian[:2, :2] = np.eye(2) # vx an
#     Jacobian[2, 3:] = np.ones((1, 4)) # d(theta) / d(q)
#     Jacobian[0, 3:] = -np.array([Ls[i:]@cosines[i:] for i in range(4)])
#     Jacobian[1, 3:] = -np.array([Ls[i:]@sines[i:] for i in range(4)])
#     Jacobian[:, 2] = Jacobian[:, 3] # theta_b and q[0] act the same
    
#     return Jacobian

if __name__ == '__main__':
    print(ik_arm([-1, 0, 2], 0, 30, [0, 1, 1, 1]))