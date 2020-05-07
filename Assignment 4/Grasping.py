#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 19:23:02 2020

@author: carter
"""

import numpy as np

#Question 6 

#for contact 1
a = np.array([[-1, 0, 0]])
b = np.array([[0, 0, -1],[0,1,0],[1,0,0]])

#for contact 2
a = np.array([[1, 0, 0]])
b = np.array([[0, 0, 1],[0,1,0],[-1,0,0]])

c = np.cross(a,b)
zero = np.zeros((3,3))
temp = np.vstack((zero,b))
Ad = np.hstack((np.vstack((b,c)),temp))

B = np.array([[0],[0],[0],[0],[0],[1]])

out = np.dot(Ad.T,B)


G = np.array([[ 0., 0],
       [ 0., 0],
       [ 0., 0],
       [1., -1],
       [ 0., 0],
       [ 0., 0]])

f = np.array([[-2], [-5]])

F = G.dot(f)

#Question 7

a = np.array([[-1, 0, 0]])
b = np.array([[0, 0, -1],[0,1,0],[1,0,0]])

#for contact 2
a = np.array([[1, 0, 0]])
b = np.array([[0, 0, 1],[0,1,0],[-1,0,0]])

c = np.cross(a,b)
zero = np.zeros((3,3))
temp = np.vstack((zero,b))
Ad = np.hstack((np.vstack((b,c)),temp))

B = np.zeros((6,3))
B[3:,:] = np.identity(3)

out = np.dot(Ad.T,B)


#combine for parts 3 and 4

G1 = np.array([[ 0.,  0.,  0.],
       [-1.,  0.,  0.],
       [ 0., -1.,  0.],
       [ 0.,  0.,  1.],
       [ 0.,  1.,  0.],
       [-1.,  0.,  0.]])

G2 = np.array([[ 0.,  0.,  0.],
       [-1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0., -1.],
       [ 0.,  1.,  0.],
       [ 1.,  0.,  0.]])

G = np.hstack((G1,G2))

#calculate contact forces with constraints
m = 1
g = 9.8
mu = 0.2
f1 = 0.5*m*g
f3 = np.sqrt(f1**2)/mu

fc1 = np.array([[-f1],[0],[f3]])
fc2 = np.array([[f1],[0],[f3]])

fc = np.vstack((fc1,fc2))

F = np.dot(G,fc)
print(F)