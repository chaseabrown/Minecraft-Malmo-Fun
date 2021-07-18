#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 19:40:56 2021

@author: chasebrown
"""

import os
os.environ["MODIN_ENGINE"] = "dask"

import json
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly as plotly
import plotly.express as px
from plotly.offline import plot
import time
import math
from numpy import ones,vstack
from numpy.linalg import lstsq



def difference(num1, num2):
    if num1>num2:
        return num1-num2
    else:
        return num2-num1



x1 = -20
x2 = 20
y1 = -20
y2 = 20
z1 = -20
z2 = 20
video_width = 864
video_height = 480



df = pd.read_csv(r'/Volumes/My Data/Minecraft AI/data/minecraftItems.csv')

itemCodes = {}
for item in df.iterrows():
    itemCodes.update({item[1]['nameOfficial']:item[1]['id']})


itemColors = {}
for item in df.iterrows():
    itemColors.update({item[1]['nameOfficial']:item[1]['color']})
itemColors.update({'player': '(222,36,52)'})

itemNames = {}
for item in df.iterrows():
    itemNames.update({item[1]['id']:item[1]['nameOfficial']})

file = open('/Volumes/My Data/Minecraft AI/logs/EyeSight.json')
data = json.load(file)



blocks = ['player']
frameData = np.zeros((len(range(x1,x2+1)), len(range(z1,z2+1))))
readableData = []
plotableData = []
otherFrameData = []
counter = 0

for frame in data:
    if frame['Life'] > 0:
        temp = {}
        temp2 = {'x':[x1,x2,x1,x2,x1,x2,x1,x2], 
                 'y':[y1,y2,y2,y1,y1,y2,y2,y1], 
                 'z':[z1,z2,z1,z2,z2,z1,z2,z1], 
                 'block':['corner', 'corner', 'corner', 'corner', 'corner', 'corner', 'corner', 'corner'], 
                 'seen':[True, True, True, True, True, True, True, True]}
        for y in range(0,len(range(y1, y2+1))):
            frameData = np.zeros((len(range(x1,x2+1)), len(range(z1,z2+1))))
            temp.update({y+y1: frameData})
            for z in range(0,len(range(z1,z2+1))):
                for x in range(0,len(range(x1,x2+1))):
                    temp2['x'].append((x-len(range(x1,x2+1))/2)+.5)
                    temp2['y'].append(y+y1)
                    temp2['z'].append(((z-len(range(z1,z2+1))/2)+.5))
                    block = frame['EyeSight'][y*len(range(x1,x2+1))*len(range(z1,z2+1)) + (x*len(range(z1,z2))+(z+x))]
                    if ((x+x1==int((x1+x2)/2)) and (y+y1==0 or y+y1==1) and (z+z1==int((z1+z2)/2))):
                        print(x,y,z)
                        temp2['block'].append('player')
                        temp2['seen'].append(True)
                    else:
                        temp2['block'].append(block)
                        temp2['seen'].append(False)
                    temp[y+y1][x][z] = itemCodes[block]
                    if (not str(itemColors[block]) == 'nan') and not block in blocks:
                        blocks.append(block)
           
        readableData.append({'blockData': temp, 'otherData':frame})
        plotableData.append({'blockData': temp2, 'otherData':frame})


    



for frame in plotableData:
    try:
        df = pd.DataFrame(data=frame['blockData'])
        
        
        yaw = frame['otherData']['Yaw']
        newYaw = yaw - 90
        pitch = -frame['otherData']['Pitch']
        print(yaw,pitch)
        x_left = -9*math.cos((newYaw * math.pi) / 180) - 14*math.sin((newYaw * math.pi) / 180)
        z_left = 14*math.cos((newYaw * math.pi) / 180) + -9*math.sin((newYaw * math.pi) / 180)
        x_right = 9*math.cos((newYaw * math.pi) / 180) - 14*math.sin((newYaw * math.pi) / 180)
        z_right = 14*math.cos((newYaw * math.pi) / 180) + 9*math.sin((newYaw * math.pi) / 180)
        
        if (225<=yaw and yaw<315):
            df.loc[((df['x'] >= x_left/z_left*df['z']) &
                    (df['x'] <= x_right/z_right*df['z'])), 'seen'] = True
            
            z_left = -9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_bottom = 14*math.cos((pitch * math.pi) / 180) + -9*math.sin((pitch * math.pi) / 180)
            z_right = 9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_top = 14*math.cos((pitch * math.pi) / 180) + 9*math.sin((pitch * math.pi) / 180)
            
            if pitch >= -45 and pitch <= 45:
                df.loc[((df['y'] <= z_left/y_bottom*df['z']) |
                        (df['y'] >= z_right/y_top*df['z'])), 'seen'] = False
            
            elif pitch < -45:
                df.loc[((df['z'] <= y_bottom/z_left*df['y']) |
                        (df['z'] >= y_top/z_right*df['y'])), 'seen'] = False
            
            elif pitch > 45:
                df.loc[((df['z'] >= y_bottom/z_left*df['y']) |
                        (df['z'] <= y_top/z_right*df['y'])), 'seen'] = False
                        
        elif (45<=yaw and yaw<135):
            df.loc[((df['x'] <= x_left/z_left*df['z']) &
                    (df['x'] >= x_right/z_right*df['z'])), 'seen'] = True
            
            z_left = -9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_bottom = 14*math.cos((pitch * math.pi) / 180) + -9*math.sin((pitch * math.pi) / 180)
            z_right = 9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_top = 14*math.cos((pitch * math.pi) / 180) + 9*math.sin((pitch * math.pi) / 180)
            
            if pitch >= -45 and pitch <= 45:
                df.loc[((df['y'] >= z_left/y_bottom*df['z']) |
                        (df['y'] <= z_right/y_top*df['z'])), 'seen'] = False
            
            elif pitch < -45:
                df.loc[((df['z'] <= y_bottom/z_left*df['y']) |
                        (df['z'] >= y_top/z_right*df['y'])), 'seen'] = False
            
            elif pitch > 45:
                df.loc[((df['z'] >= y_bottom/z_left*df['y']) |
                        (df['z'] <= y_top/z_right*df['y'])), 'seen'] = False
                        
        elif (315<=yaw or yaw<45):
            df.loc[((df['z'] >= z_left/x_left*df['x']) &
                    (df['z'] <= z_right/x_right*df['x'])), 'seen'] = True
            
            x_left = -9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_bottom = 14*math.cos((pitch * math.pi) / 180) + -9*math.sin((pitch * math.pi) / 180)
            x_right = 9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_top = 14*math.cos((pitch * math.pi) / 180) + 9*math.sin((pitch * math.pi) / 180)
            
            if pitch >= -45 and pitch <= 45:
                df.loc[((df['y'] >= x_left/y_bottom*df['x']) |
                        (df['y'] <= x_right/y_top*df['x'])), 'seen'] = False
           
            elif pitch < -45:
                df.loc[((df['x'] <= y_bottom/x_left*df['y']) |
                        (df['x'] >= y_top/x_right*df['y'])), 'seen'] = False
            
            elif pitch > 45:
                df.loc[((df['x'] >= y_bottom/x_left*df['y']) |
                        (df['x'] <= y_top/x_right*df['y'])), 'seen'] = False
            
        elif (135<=yaw and yaw<225):
            df.loc[((df['z'] <= z_left/x_left*df['x']) &
                    (df['z'] >= z_right/x_right*df['x'])), 'seen'] = True
            x_left = -9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_bottom = 14*math.cos((pitch * math.pi) / 180) + -9*math.sin((pitch * math.pi) / 180)
            x_right = 9*math.cos((pitch * math.pi) / 180) - 14*math.sin((pitch * math.pi) / 180)
            y_top = 14*math.cos((pitch * math.pi) / 180) + 9*math.sin((pitch * math.pi) / 180)
                
            if pitch >= -45 and pitch <= 45:
                df.loc[((df['y'] <= x_left/y_bottom*df['x']) |
                        (df['y'] >= x_right/y_top*df['x'])), 'seen'] = False
            
            elif pitch < -45:
                df.loc[((df['x'] <= y_bottom/x_left*df['y']) |
                        (df['x'] >= y_top/x_right*df['y'])), 'seen'] = False
            
            elif pitch > 45:
                df.loc[((df['x'] >= y_bottom/x_left*df['y']) |
                        (df['x'] <= y_top/x_right*df['y'])), 'seen'] = False
            
    
        df.loc[((df['x'] == 0) & ((df['y'] == 0) | (df['y'] == 1)) & (df['z'] == 0)), 'block'] = 'player'
        color_discrete_map = {'player': 'rgb(222,36,52)', 'seen': 'rgb(256,256,256)', 'line': 'rgb(34,139,34)', 'north': 'rgb(222,36,52)',
                              'south': 'rgb(20,26,209)', 'west': 'rgb(209,196,20)', 'east': 'rgb(34,139,34)'}
        
        for i in blocks:
            color_discrete_map.update({i:'rgb' + itemColors[i]})
            
        #indexNames = df[(df['block'] == 'air')].index
        #df.drop(indexNames , inplace=True)
        df.loc[(df['block'] == 'corner'), 'seen'] = True
        df.loc[(df['block'] == 'player'), 'seen'] = True
        
        df.loc[(df['seen'] == False), 'block'] = 'seen'
        indexNames = df[(df['block'] == 'seen')].index
        df.drop(indexNames , inplace=True)
        fig = px.scatter_3d(df, x='z', y='x', z='y',
                          color='block', color_discrete_map=color_discrete_map)
            
        
        name = 'default'
        plot(fig)
        
        #input("Press Enter for Next Frame...")
            
        """
        indexNames = df[(df['x'] < (df['z']+1)/math.tan(angle * math.pi / 180))].index
        df.loc[indexNames, 'block'] = "seen"
        indexNames = df[(df['x'] > -(df['z']+1)/math.tan(angle * math.pi / 180))].index
        df.loc[indexNames, 'block'] = "seen"
        indexNames = df[(df['y']-1 < (df['z']+1)/math.tan(angle * math.pi / 180))].index
        df.loc[indexNames, 'block'] = "seen"
        indexNames = df[(df['y']-1 > -(df['z']+1)/math.tan(angle * math.pi / 180))].index
        df.loc[indexNames, 'block'] = "seen"
        df.loc[((df['x'] == 0) & ((df['y'] == 0) | (df['y'] == 1)) & (df['z'] == -1)), 'block'] = 'player'
        indexNames = df[(df['block'] == 'seen') ].index
        df.drop(indexNames , inplace=True)
        
        
        
        slopes = []
        startX = 0
        startY = 1
        startZ = -1
        for point in df.iterrows():
            point = point[1]
            if not point['block'] == 'player' and not point['block'] == 'seen':
                slopeX = (point['x']-startX)/(point['z'])
                slopeY = (point['y']-startY)/(point['z'])
                slopes.append({'x': slopeX, 'y': slopeY})
        
        for slope in slopes:
            for z in range(2,22):
                z=-z
                if (not len(df.loc[((df['x'] == startX + int(slope['x']*z)) & ((df['y'] == startY + int(slope['y']*z))) & (df['z'] == z)), 'block'])==0):
                    df.loc[((df['x'] == startX + int(slope['x']*z)) & ((df['y'] == startY + int(slope['y']*z))) & (df['z'] == z)), 'block'] = 'line2'
                    break
        """
    except Exception as e:
        print(e)
