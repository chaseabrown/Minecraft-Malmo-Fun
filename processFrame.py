#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:57:39 2021

@author: chasebrown
"""

import json
import numpy as np
import cv2
import pandas as pd
import os
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
from matplotlib import image
from matplotlib import pyplot
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img
from keras.preprocessing.image import save_img
import open3d as o3d
import mysql.connector as connector
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour


frame = 33
life = 1
while True:
    
    video_width = 860
    video_height = 480
    
    
    
    path = '/Volumes/My Data/Minecraft AI/recordings/Single Frames/' + str(life)
    filename = "frame" + str(frame) + ".png"
    
    image = Image.open(path + '/video_frames/' + filename)
    
    depthImage = Image.open(path + '/depth_frames/' + filename)
    depth = np.array(depthImage)
    changedTracker = np.empty((video_height,video_width))
    img_array = np.array(image)
    
    
    
    for y in range(0, video_height):
        for x in range(0, video_width):
            try:
                if (depth[y][x] == depth[y+1][x] and depth[y][x] == depth[y-1][x] and not depth[y][x] == depth[y][x+1]) and depth[y][x]<254:
                    img_array[y][x][0] = 0
                    img_array[y][x][1] = 255
                    img_array[y][x][2] = 255
                    changedTracker[y][x] = 20
                elif (depth[y][x] == depth[y][x+1] and depth[y][x] == depth[y][x-1] and not depth[y][x] == depth[y+1][x]) and depth[y][x]<254:
                    img_array[y][x][0] = 150
                    img_array[y][x][1] = 0
                    img_array[y][x][2] = 255
                    changedTracker[y][x] = -20
                elif (depth[y][x] == depth[y][x+1] and depth[y][x] == depth[y][x-1] and depth[y][x] == depth[y+1][x] and depth[y][x] == depth[y-1][x]) and depth[y][x]<254:
                    img_array[y][x][0] = 0
                    img_array[y][x][1] = 255
                    img_array[y][x][2] = 255
                    changedTracker[y][x] = 20
                else:
                    changedTracker[y][x] = 0
            
            except:
                changedTracker[y][x] = 0
    
    
    
    img_pil = Image.fromarray(img_array)
    
    img_pil.save("/Volumes/My Data/Minecraft AI/recordings/Single Frames/" + str(life) + "/depth_frames/surfaces/" + filename)
    frame += 1
    



life = 1
frame = 1
video_width = 860
video_height = 480

while(True):
    path = '/Volumes/My Data/Minecraft AI/recordings/Single Frames/' + str(life)
    filename = "frame" + str(frame) + ".png"
    
    im_pil = Image.open(path + '/video_frames/' + filename)
    im_pil2 = Image.open(path + '/depth_frames/' + filename)
    im_pil3 = Image.open(path + '/colormap_frames/' + filename)

    im_pil4 = im_pil3.filter(ImageFilter.FIND_EDGES)
    
    array = np.array(im_pil4)
    array2 = np.array(im_pil)
    array3 = np.array(im_pil)
    array4 = np.array(im_pil)
    array5 = np.array(im_pil)
    array6 = np.array(im_pil3)
    array7 = np.array(im_pil3)
    outline = np.empty_like(array)
    
    depth = np.array(im_pil2)
    for y in range(0, video_height):
        for x in range(0, video_width):
            outline[y][x][0] = 0
            outline[y][x][1] = 0
            outline[y][x][2] = 0
            if (not (int(array7[y][x][0]) == 23 and int(array7[y][x][1]) == 185 and int(array7[y][x][2]) == 0)) and (not (int(array7[y][x][0]) == 232 and int(array7[y][x][1]) == 209 and int(array7[y][x][2]) == 0)) and (not (int(array7[y][x][0]) == 209 and int(array7[y][x][1]) == 23 and int(array7[y][x][2]) == 23)) and (not (int(array7[y][x][0]) == 139 and int(array7[y][x][1]) == 46 and int(array7[y][x][2]) == 46)):
                if not (array[y][x][0] == 0 and array[y][x][1] == 0 and array[y][x][2] == 0):
                    array2[y][x][0] = int(depth[y][x])
                    array2[y][x][1] = 0
                    array2[y][x][2] = 255
                    array4[y][x][0] = int(depth[y][x])
                    array4[y][x][1] = 0
                    array4[y][x][2] = 255
                    outline[y][x][0] = int(depth[y][x])
                    outline[y][x][1] = 0
                    outline[y][x][2] = 255
                    array6[y][x][0] = 0
                    array6[y][x][1] = 0
                    array6[y][x][2] = 0
                try:
                    if abs(int(depth[y][x])-int(depth[y+1][x])) > 3 or abs(int(depth[y][x])-int(depth[y][x+1])) > 3 :
                        array3[y][x][0] = int(depth[y][x])
                        array3[y][x][1] = 255
                        array3[y][x][2] = 0
                        array4[y][x][0] = int(depth[y][x])
                        array4[y][x][1] = 0
                        array4[y][x][2] = 255
                        outline[y][x][0] = int(depth[y][x])
                        outline[y][x][1] = 0
                        outline[y][x][2] = 255
                        array6[y][x][0] = 0
                        array6[y][x][1] = 0
                        array6[y][x][2] = 0
                    elif (abs(int(depth[y][x-3])-int(depth[y][x])) > 0 and abs(int(depth[y][x])-int(depth[y][x+10]))==0) and (abs(int(depth[y][x-2])-int(depth[y][x])) == 0 and abs(int(depth[y][x])-int(depth[y][x+5]))==0) and (abs(int(depth[y][x-1])-int(depth[y][x])) == 0 and abs(int(depth[y][x])-int(depth[y][x+1]))==0):
                        array5[y][x][0] = int(depth[y][x])
                        array5[y][x][1] = 0
                        array5[y][x][2] = 0
                        array4[y][x][0] = int(depth[y][x])
                        array4[y][x][1] = 0
                        array4[y][x][2] = 255
                        outline[y][x][0] = int(depth[y][x])
                        outline[y][x][1] = 0
                        outline[y][x][2] = 255
                        array6[y][x][0] = 0
                        array6[y][x][1] = 0
                        array6[y][x][2] = 0
                except Exception as e:
                    pass
            

            
            
    
    

    im_pil6 = Image.fromarray(array2)    
    im_pil5 = Image.fromarray(array3)    
    im_pil4 = Image.fromarray(array4)
    im_pil7 = Image.fromarray(array5)
    im_pil8 = Image.fromarray(array6)

    outline = Image.fromarray(outline)

    new_image = Image.new('RGB',(3*video_width, 3*video_height), (255,255,255))
    new_image.paste(im_pil,(0,0))
    new_image.paste(im_pil2,(video_width,0))
    new_image.paste(im_pil3,(2*video_width,0))
    
    new_image.paste(im_pil5,(0,video_height))
    new_image.paste(im_pil6,(video_width,video_height))
    new_image.paste(im_pil7,(2*video_width,video_height))
    
    new_image.paste(im_pil4,(0,2*video_height))
    new_image.paste(outline,(video_width,2*video_height))
    new_image.paste(im_pil8,(2*video_width,2*video_height))


    new_image.save(path + "/combo/" + filename)
    frame+=1


life = 2
frame = 11
path = '/Volumes/My Data/Minecraft AI/recordings/Single Frames/' + str(life)
filename = "frame" + str(frame) + ".png"
video_width = 860
video_height = 480

mydb = connector.connect(
    host="localhost",
    user="root",
    password="password", 
    database="minecraft"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM observations where life=" + str(life) + " AND frame=" + str(frame) + ";")
data = []
for x in mycursor:
    data = x
XPos = data[3]
YPos = data[4]
ZPos = data[5]
pitch = data[6]
yaw = data[7]
mycursor.close()
mydb.close()




color_raw = o3d.io.read_image(path + '/video_frames/' + filename)
depth_raw = o3d.io.read_image(path + '/depth_frames/' + filename)

rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)



plt.subplot(1, 2, 1)
plt.title('Redwood grayscale image')
plt.imshow(rgbd_image.color)
plt.subplot(1, 2, 2)
plt.title('Redwood depth image')
plt.imshow(rgbd_image.depth)
plt.show()


pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
    rgbd_image,
    o3d.camera.PinholeCameraIntrinsic(width = video_width, height=video_height, fx = 255, fy = 255, cx = 10, cy =10))
# Flip it, otherwise the pointcloud will be upside down
pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
o3d.visualization.draw_geometries([pcd])
