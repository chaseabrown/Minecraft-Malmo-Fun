#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 12:29:39 2021

@author: chasebrown
"""

from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Sample to demonstrate use of the DefaultWorldGenerator, ContinuousMovementCommands, timestamps and ObservationFromFullStats.
# Runs an agent in a standard Minecraft world, randomly seeded, uses timestamps and observations
# to calculate speed of movement, and chooses tiny "programmes" to execute if the speed drops to below a certain threshold.
# Mission continues until the agent dies.

from builtins import range
import MalmoPython
import random
import sys
import time
import datetime
import json
from random import random, randint
import random as rand
import malmoutils
import json
import re
from PIL import Image
import numpy as np
from io import BytesIO
import logging
from builtins import range
from past.utils import old_div


import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
os.environ["MALMO_XSD_PATH"] = "/Users/chasebrown/MalmoPlatform/Schemas"
from Models.DQNA import DQNAgent
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import math

malmoutils.fix_print()


def processFrame(life, depthFrame, colorFrame, frameNumber, data):
    
    path = '/Volumes/My Data/Minecraft AI/recordings/Single Frames/' + str(life)
    filename = "frame%d.png" % frameNumber
    
    image = Image.frombytes('RGB', (colorFrame.width, colorFrame.height), bytes(colorFrame.pixels))
    image.save(path + "/colormap_frames/frame%d.png" % frameNumber)
    
    data = data[-1]
    
    mydb = connector.connect(
      host="localhost",
      user="root",
      password="password", 
      database="minecraft"
    )
    mycursor = mydb.cursor()
    sql = "INSERT IGNORE INTO observations (life, frame, XPos, YPos, ZPos, pitch, yaw) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = ( str(life), 
            str(frameNumber), 
            str(data['XPos']), 
            str(data['YPos']), 
            str(data['ZPos']),
            str(data['Pitch']), 
            str(data['Yaw']))
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()

    image = Image.frombytes('RGBA', (depthFrame.width, depthFrame.height), bytes(depthFrame.pixels))
    
    img_array = np.array(image)
    
    filename2 = "depth%d.npy" % frameNumber
    depth = img_array[:,:,3]
    np.save(path + '/depth_frames/' + filename2, depth)
    image2 = Image.fromarray(depth)
    image2.save(path + '/depth_frames/' + filename)

    
    img_rgb = image.convert("RGB")
    
    img_rgb.save(path + '/video_frames/' + filename)
    

def GetMissionXML(generatorString):
    ''' Build an XML mission string that uses the DefaultWorldGenerator.'''
    
    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>Normal life</Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
                <DefaultWorldGenerator seed="654616485" />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Adam</Name>
            <AgentStart>
                <Inventory>
                    <InventoryBlock slot="0" type="glowstone" quantity="63"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="180"/>                
                <ObservationFromFullStats/>
                <ObservationFromGrid>
                      <Grid name="EyeSight">
                        <min x="-5" y="-5" z="-5"/>
                        <max x="5" y="5" z="5"/>
                      </Grid>
                 </ObservationFromGrid>
                 <AgentQuitFromTimeUp timeLimitMs="10000"/>
            </AgentHandlers>
        </AgentSection>
        <AgentSection mode="Creative">
            <Name>Chase</Name>
            <AgentStart>
                <Inventory>
                    <InventoryBlock slot="0" type="glowstone" quantity="63"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="180"/>                
                <ObservationFromFullStats/>
                <ObservationFromGrid>
                      <Grid name="EyeSight">
                        <min x="-5" y="-5" z="-5"/>
                        <max x="5" y="5" z="5"/>
                      </Grid>
                 </ObservationFromGrid>
                 <AgentQuitFromTimeUp timeLimitMs="10000"/>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''
  
def generateWorld(life, directory, generatorString):
    print("Launching Life: " + str(life))
    newPath = directory + str(life)
    if not os.path.exists(newPath):
        os.makedirs(newPath)
        os.makedirs(newPath+'/video_frames/')
        os.makedirs(newPath+'/depth_frames/')
        os.makedirs(newPath+'/colormap_frames/')
        os.makedirs(newPath+'/depth_frames/surfaces/')
        os.makedirs(newPath+'/combo/')
    
    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10001))

    
    agent_host = MalmoPython.AgentHost()
    player = MalmoPython.AgentHost()
    malmoutils.parse_command_line(agent_host)
    
    my_mission = MalmoPython.MissionSpec(GetMissionXML(generatorString), True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    
    if agent_host.receivedArgument("test"):
        my_mission.timeLimitInSeconds(20) # else mission runs forever
    
    # Attempt to start the mission:
    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_client_pool, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission",e)
                print("Is the game running?")
                exit(1)
            else:
                time.sleep(2)    
    
  
    return agent_host, my_mission_record, my_client_pool



# Variety of strategies for dealing with loss of motion:
commandSequences=[
    "move 0",
    "move 1",
    "move -1",
    "jump 1",
    "jump 0",
    "turn 0",
    "turn .5",
    "turn -.5"]

commandsCurrent = {
    "move": "0",
    "jump": "0",
    "attack": "0",
    "use": "0",
    "strafe": "0",
    "pitch": "0",
    "turn": "0"}

life = 0
model = 'DQNA'
testName = 'template'
directory = '/Volumes/My Data/Minecraft AI/recordings/' + model + '-' + testName + '/'
generatorString = '3;7,59*1,3*3,2;1;stronghold,biome_1,village,decoration,dungeon,lake,mineshaft,lava_lake'
state_size = 1331 + 9
action_size = len(commandSequences)
first_action = True
action = 0
state = np.zeros(state_size)



output_dir = 'model_output/' + model + '-' + testName + '/'
batch_size = 64
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

adams_mind = DQNAgent(state_size, action_size)

while(True):
    adams_body, my_mission_record = generateWorld(life, directory, generatorString)
    
    # Wait for the mission to start:
    world_state = adams_body.getWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = adams_body.getWorldState()
    
    currentSequence="move 0;"    # start off by moving
    currentSpeed = 0.0
    distTravelledAtLastCheck = 0.0
    timeStampAtLastCheck = datetime.datetime.now()
    cyclesPerCheck = 10 # controls how quickly the agent responds to getting stuck, and the amount of time it waits for on a "wait" command.
    currentCycle = 0
    waitCycles = 0
    lastBlockSeen = []
    startingX = 0
    startingZ = 0
    lastDist = 0
    lastPitch = 0
    lastYaw = 0
    lastReward = 0
    dist = 0
    firstTime = True
    while world_state.is_mission_running:
        world_state = adams_body.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            obvsText = world_state.observations[-1].text
            data = json.loads(obvsText)
            lastBlockSeen = data['EyeSight']
            lastPitch = data['Pitch']
            lastYaw = data['Yaw']
            if firstTime:
                startingX = data['XPos']
                startingZ = data['ZPos']
                firstTime = False
            lastDist = dist
            dist = math.sqrt((startingX - data['XPos']) ** 2 + (startingZ - data['ZPos']) ** 2)    #... containing a "DistanceTravelled" field (amongst other things).

                    
            if not first_action:
                next_state = np.zeros(state_size)
                last = 0
                for i in range(0, len(lastBlockSeen)):
                    if lastBlockSeen[i] == 'air':
                        next_state[i] == 0.0
                    elif lastBlockSeen[i] == 'water':
                        next_state[i] == 1.0
                    elif lastBlockSeen[i] == 'lava':
                        next_state[i] == 3.0
                    else:
                        next_state[i] == 2.0
                    last = i
                next_state[last+1] = int(commandsCurrent['move'])
                next_state[last+2] = int(commandsCurrent['jump'])
                next_state[last+3] = int(commandsCurrent['attack'])
                next_state[last+4] = int(commandsCurrent['use'])
                next_state[last+5] = int(commandsCurrent['strafe'])
                next_state[last+6] = float(commandsCurrent['pitch'])
                next_state[last+7] = float(commandsCurrent['turn'])
                next_state[last+8] = lastPitch
                next_state[last+9] = lastYaw

                next_state = np.reshape(next_state, [1, state_size])
                
                reward = dist - lastDist
                lastReward = reward
                done = False
                
                adams_mind.remember(state, action, reward, next_state, done)
            
            state = np.zeros(state_size)
            timeSinceCommand = 0
            first_action = False
            last = 0
            for i in range(0, len(lastBlockSeen)):
                if lastBlockSeen[i] == 'air':
                    state[i] == 0.0
                elif lastBlockSeen[i] == 'water':
                    state[i] == 1.0
                elif lastBlockSeen[i] == 'lava':
                    state[i] == 3.0
                else:
                    state[i] == 2.0
                last = i
            state[last+1] = int(commandsCurrent['move'])
            state[last+2] = int(commandsCurrent['jump'])
            state[last+3] = int(commandsCurrent['attack'])
            state[last+4] = int(commandsCurrent['use'])
            state[last+5] = int(commandsCurrent['strafe'])
            state[last+6] = float(commandsCurrent['pitch'])
            state[last+7] = float(commandsCurrent['turn'])
            state[last+8] = lastPitch
            state[last+9] = lastYaw
            
            state = np.reshape(state, [1, state_size])
            
            action = adams_mind.act(state)
            
            adams_body.sendCommand(commandSequences[action])    # Send the command to Minecraft.  
            commandsCurrent[commandSequences[action].split(' ')[0]] = commandSequences[action].split(' ')[1]
            
            if len(adams_mind.memory) > batch_size:
                adams_mind.replay(batch_size) 
            
            print("Last Reward: " + str(lastReward) + " | Adam Chose: " + commandSequences[action])
            time.sleep(.5)
    
    next_state = np.zeros(state_size)
    last = 0
    for i in range(0, len(lastBlockSeen)):
        if lastBlockSeen[i] == 'air':
            next_state[i] == 0.0
        elif lastBlockSeen[i] == 'water':
            next_state[i] == 1.0
        elif lastBlockSeen[i] == 'lava':
            next_state[i] == 3.0
        else:
            next_state[i] == 2.0
            last = i
    next_state[last+1] = int(commandsCurrent['move'])
    next_state[last+2] = int(commandsCurrent['jump'])
    next_state[last+3] = int(commandsCurrent['attack'])
    next_state[last+4] = int(commandsCurrent['use'])
    next_state[last+5] = int(commandsCurrent['strafe'])
    next_state[last+6] = float(commandsCurrent['pitch'])
    next_state[last+7] = float(commandsCurrent['turn'])
    next_state[last+8] = lastPitch
    next_state[last+9] = lastYaw
    next_state = np.reshape(next_state, [1, state_size])
    
    reward = -10
    done = False
    
    adams_mind.remember(state, action, reward, next_state, done)
        
    # Mission has ended.

    