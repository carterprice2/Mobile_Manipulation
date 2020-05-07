#!/usr/bin/env python
"""main.py
Main code loop for MM8803 final project

@author Gerry and Carter
"""

from Communication import Robot, ImageFetcher
from Kinematics import ik, R, cosd, sind
from mm_image_processing import get_center_width_height

import numpy as np
import time
import cv2

DESIRED_THETA = np.arange(0, 360, 60)
DESIRED_PHI = np.array([30.])
DESIRED_DIST = 1.2

def calc_x_openloop(theta, phi, plantx, dist):
    x = np.array([
        dist * sind(phi) * cosd(theta),
        dist * sind(phi) * sind(theta),
        dist * cosd(phi)
    ])
    return plantx - x

def calc_x_closedloop(prevX, theta, phi, d_desired, img):
    cX, cY, w, h = get_center_width_height(img)
    # convert pixel coordinates to camera frame coordinates
    h_img = np.size(img, axis=1)
    fov = 60
    w_ang, h_ang = w * fov / h_img, h * fov / h_img
    true_d = 1
    d_actual = (true_d / 2) / np.tan(np.deg2rad(max(w_ang, h_ang) / 2))
    px2units = true_d / max(w, h)
    error_camframe = np.reshape([-(d_actual-d_desired),
                                 -(cX - np.size(img, axis=0)/2) * px2units,
                                 -(cY - np.size(img, axis=1)/2) * px2units], (3, 1))
                                 # define camera frame so that x->y, y->z, z->-x
                                 # also image is rotated 180 so x and y get negative
    print(error_camframe)

    # convert camera coordinates to world coordinates
    Rphi = np.array([[cosd(phi), 0, -sind(phi)],
                     [0, 1, 0],
                     [sind(phi), 0, cosd(phi)]])
    Rtheta = np.array([[cosd(theta), -sind(theta), 0],
                       [sind(theta), cosd(theta), 0],
                       [0, 0, 1]])
    error_worldframe = Rtheta @ Rphi @ error_camframe
    print(error_worldframe)
    
    # return new setpoint pos
    gain = 0.9
    return prevX - error_worldframe.flatten() * gain

#def follow_trajectory( old_x, new_x, smoothness = 0.1): #, #theta, phi, robot):
#    diff = new_x - old_x
#    print(diff)
#    num_steps = np.linalg.norm(diff)/smoothness
#    print(num_steps)
#    step = diff/num_steps
#    for i in range(int(num_steps)):
#        current = old_x + step*i
#        print(current)
#        #q = ik(current,theta,phi)
#        #robot.command_robot(q[0:3], q[3:7], False)
    
def main():
    robot = Robot()
    fetcher = ImageFetcher()
    fetcher.start()
    robot.command_robot([0,0,0], [0,0,0,0], False) # get a good tcp connection
    time.sleep(1)
    # for each desired view angle
    for phi in DESIRED_PHI:
        for theta in DESIRED_THETA:
            # first go to nominal position
            x = calc_x_openloop(theta, phi, [0, 0, 7], 3)
            q = ik(x, theta, phi)
            robot.command_robot(q[0:3], q[3:7], True)
            #img, _, _ = fetcher.get_image()
            # then do visual servoing until we get close enough
            while True:
                img, _, _ = fetcher.get_image()
                prev_x = x
                try: 
                    x = calc_x_closedloop(x, theta, phi, DESIRED_DIST, img)
                    if np.linalg.norm(x - prev_x) / np.linalg.norm(x) < 0.01:
                        print("Visual Servoing converged, proceeding.")
                        cv2.imwrite("SfM_pics/" + str(x) + ".png", img)
                        break
                    q = ik(x, theta, phi)
                    robot.command_robot(q[0:3], q[3:7], True)
                except:
                    print("something broke, most likely the lettuce was not in the field of view")
                    break
    robot.__del__()

if __name__ == '__main__':
    main()