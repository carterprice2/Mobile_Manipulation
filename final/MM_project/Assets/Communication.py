#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:38:44 2020

Description: communication class with Unity server, handles outgoing connections to robot and also
    reads images from folder.

@author: Carter and Gerry
"""

#test Communication with Unity server

import socket
import time
import cv2
from threading import Thread

'''class Robot handles outgoing connections to unity server.
'''
class Robot:
    def __init__(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 6340
        BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(1)

        self.conn, self.addr = self.s.accept()
        print('Connection address:', self.addr)

        self.last_pos = ([0,0,0], [0,0,0,0])
        self.last_pos_time = None

    '''command_robot - sends commands to the unity robot
    Args:
        base - 3-tuple of base x, y, theta
        joints - 4-tuple of joint angles
        pic - boolean whether or not to activate the camera
    '''
    def command_robot(self, base, joints, pic=False):
        base = base[0:3]
        joints = joints[0:4]
        print("({:7.3f}, {:7.3f}, {:7.3f}), ({:7.3f}, {:7.3f}, {:7.3f}, {:7.3f}), {:d}".format(
                *base, *joints, pic))
        base[2] = base[2]+45
        joints[0] = -joints[0] + 90
        joints[1] = -joints[1]
        joints[2] = -joints[2]
        joints[3] = -joints[3]
        data = " {:f},{:f},{:f},{:f},{:f},{:f},{:f},{}   ".format(
                *base, *joints, "false").encode()
        self.conn.send(data)
        if pic:
            print('testy')
            time.sleep(0.5) # wait to arrive at position
            data = " {:f},{:f},{:f},{:f},{:f},{:f},{:f},{}   ".format(
                    *base, *joints, "true").encode()
            self.conn.send(data) # take picture
            time.sleep(0.05)     # wait for picture to be taken
            data = " {:f},{:f},{:f},{:f},{:f},{:f},{:f},{}   ".format(
                    *base, *joints, "false").encode()
            self.conn.send(data) # don't take more pictures

        # self.last_pos = (base, joints)
    
    def __del__(self):
        print('destroying robot object')
        self.conn.close()

'''ImageFetcher - class to continually import newest images from folder
usage:
    fetcher = ImageFetcher()
    fetcher.start()
    # do stuff
    img, time, index = fetcher.get_image()
    # do stuff
    fetcher.stop()

optionally pass a callback to the constructor which takes as a single argument img
'''
class ImageFetcher:
    def __init__(self, callback=None):
        self.getting_images = False
        self.last_picture = None
        self.last_picture_time = None
        self.last_picture_ind = -1
        self.callback = callback
        # clear directory
        import os
        import glob
        files = glob.glob('../../images/*')
        for f in files:
            os.remove(f)
    
    def start(self):
        self.getting_images = True
        self.t = Thread(target=self.get_imgs)
        self.t.start()
    def stop(self):
        self.getting_images = False
    def get_image(self, blocking=True):
        if blocking:
            while self.last_picture is None:
                time.sleep(0.1)
        return self.last_picture, self.last_picture_time, self.last_picture_ind

    def get_imgs(self):
        while self.getting_images:
            self.get_img()
        print('stopped getting images')
    def get_img(self):
        img = None
        while img is None and self.getting_images:
            img = cv2.imread('../../images/{:d}.png'.format(self.last_picture_ind+1), cv2.IMREAD_COLOR)
        print('got image')
        self.last_picture = img
        self.last_picture_time = time.time()
        self.last_picture_ind = self.last_picture_ind + 1
        if self.callback is not None:
            self.callback(img)
        return self.last_picture

if __name__=='__main__':
    fetcher = ImageFetcher()
    fetcher.start()
    robot = Robot()
    robot.command_robot([0, 0, 0], [0, 0, 0, 0], pic=False)
    time.sleep(1)
    # input()
    robot.command_robot([1, 0, 0], [0, 0, 0, 0], pic=False)
    time.sleep(1)
    robot.command_robot([0, 0, 0], [90, 0, 0, 0], pic=False)
    time.sleep(1)
    robot.command_robot([0, 0, 0], [0, 90, 0, 0], pic=False)
    time.sleep(1)
    robot.command_robot([0, 0, 0], [0, 0, 90, 0], pic=False)
    time.sleep(1)
    robot.command_robot([0, 0, 0], [0, 0, 0, 90], pic=False)
    time.sleep(1)
    robot.command_robot([0, 0, 0], [0, 0, 0, 0], pic=False)
    time.sleep(1)
    for i in range(10):
        robot.command_robot([0, -1, 0], [0, -90+i*18, 0, 0], True)
        time.sleep(0.3)
    time.sleep(1)
    robot.command_robot([1, 0, 0], [0, 0, 5, 0], True)
    time.sleep(3)
    fetcher.stop()