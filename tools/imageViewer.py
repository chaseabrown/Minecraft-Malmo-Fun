#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 16:39:11 2021

@author: chasebrown
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import matplotlib.cm as cm
from PIL import Image, ImageFilter


life = 1
frame = 33
path = '/Volumes/My Data/Minecraft AI/recordings/Single Frames/' + str(life)
filename = "frame" + str(frame) + ".png"

img = mpimg.imread(path + '/video_frames/' + filename)


# Make an array with ones in the shape of an 'X'
depthImage = Image.open(path + '/depth_frames/' + filename)
depth = np.array(depthImage)

fig = plt.figure()
ax1 = fig.add_subplot(121)
# Bilinear interpolation - this will look blurry
ax1.imshow(img)

ax2 = fig.add_subplot(122)

def onclick(event):
    if event.xdata != None and event.ydata != None:
        a = depth[int(event.ydata)-2:int(event.ydata)+3, int(event.xdata)-2:int(event.xdata)+3]
        
        print(event.xdata, event.ydata)
        ax2.imshow(a, interpolation='nearest', cmap=cm.Greys_r)
        fig.canvas.draw()
        fig.canvas.flush_events()
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()