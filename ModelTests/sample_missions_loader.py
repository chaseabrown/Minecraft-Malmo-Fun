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

# Sample mission loader
# Used to check the mission repository

from builtins import range
import MalmoPython
import sys
import time
import random
import malmoutils
from PIL import Image


import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
os.environ["MALMO_XSD_PATH"] = "/Users/chasebrown/MalmoPlatform/Schemas"
from Models.DQNA import DQNAgent
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

malmoutils.fix_print()

# -- set up the mission -- #
missionFiles = [
    './Sample_missions/default_world_1',                # 0: Survive and find gold, diamond or redstone!
    './Sample_missions/default_flat_1',                 # 1: Move to a wooden hut in a snow tempest!
    './Sample_missions/tricky_arena_1',                 # 2: Mind your step to the redstone!
    './Sample_missions/eating_1',                       # 3: Eat a healthy diet!
    './Sample_missions/cliff_walking_1',                # 4: Burning lava!
    './Sample_missions/mazes/maze_1',                   # 5: Get a-mazed! A simple maze.
    './Sample_missions/mazes/maze_2',                   # 6: Get more a-mazed! A complex maze.
    './Sample_missions/classroom/basic',                # 7: Grab the treasure! Single small room
    './Sample_missions/classroom/obstacles',            # 8: The apartment! Some rooms
    './Sample_missions/classroom/simpleRoomMaze',       # 9: Some rooms making a maze (not with maze decorator)
    './Sample_missions/classroom/attic',                # 10: Lava, libraries, incomplete staircase, goal is in the attic
    './Sample_missions/classroom/vertical',             # 11: Need to go up
    './Sample_missions/classroom/complexity_usage',     # 12: Big rooms generator with doors, pillars, a house
    './Sample_missions/classroom/medium',               # 13: Hotel California: big rooms with doors, ladders....
    './Sample_missions/classroom/hard']                 # 14: Buckingham Palace: big rooms with doors, easy to get lost, ...

mission_file_no_ext = missionFiles[7]

agent_host = MalmoPython.AgentHost()

try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)
if agent_host.receivedArgument("test"):
    exit(0) # TODO: discover test-time folder names

mission_file = mission_file_no_ext + ".xml"
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    
# Set up a recording 
my_mission_record = MalmoPython.MissionRecordSpec(mission_file_no_ext + ".tgz")
my_mission_record.recordRewards()
my_mission_record.recordMP4(24,400000)
# Attempt to start a mission
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

total_reward = 0.0

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
    "turn": "0"}

state_size = 320*240 + len(commandsCurrent)
action_size = len(commandSequences)
model = 'DQNA'
testName = 'template'
output_dir = 'model_output/' + model + '-' + testName + '/'
batch_size = 64
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

adams_mind = DQNAgent(state_size, action_size)
img_array = ''
# main loop:
while world_state.is_mission_running:
    world_state = agent_host.getWorldState()
    
    if world_state.number_of_video_frames_since_last_state > 0:
            frame = world_state.video_frames[-1]
            image = Image.frombytes('RGB', (frame.width, frame.height), bytes(frame.pixels))
            img_array = np.array(image)
            
            

                    
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
                next_state[last+3] = float(commandsCurrent['turn'])

                next_state = np.reshape(next_state, [1, state_size])
                
                for reward in world_state.rewards:
                    total_reward += reward.getValue()
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
    
    for reward in world_state.rewards:
        print("Summed reward:",reward.getValue())
        total_reward += reward.getValue()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
print("Total reward = " + str(total_reward))
