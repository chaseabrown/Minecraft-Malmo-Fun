#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 00:25:45 2021

@author: chasebrown
"""

#Install Dataset
#import minerl
#minerl.data.download(directory="/Volumes/My Data/Minecraft AI/data")

import gym
import minerl
import logging
import plotly.graph_objs as go
import plotly as plotly
import plotly.express as px
import pandas as pd
import numpy as np
import time
import tqdm
from sklearn.cluster import KMeans
import os




os.environ["MINERL_DATA_ROOT"] = "/Volumes/My Data/Minecraft AI/data/"

def figures_to_html(figs, filename="dashboard.html"):
    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")

def main():
    
    dat = minerl.data.make('MineRLTreechopVectorObf-v0')

    # Load the dataset storing 1000 batches of actions
    act_vectors = []
    for a, act, b, c,d in tqdm.tqdm(dat.batch_iter(16, 32, 2, preload_buffer_size=20)):
        act_vectors.append(act['vector'])
        
        if len(act_vectors) > 1000:
            break
    
    # Reshape these the action batches
    acts = np.concatenate(act_vectors).reshape(-1, 64)
    kmeans_acts = acts[:100000]
    
    # Use sklearn to cluster the demonstrated actions
    kmeans = KMeans(n_clusters=32, random_state=0).fit(kmeans_acts)
    
    i, net_reward, done, env = 0, 0, False, gym.make('MineRLTreechopVectorObf-v0')
    env.make_interactive(port=6666, realtime=True)

    # reset the env
    env.reset()
    while not done:
        # Let's use a frame skip of 4 (could you do better than a hard-coded frame skip?)
        if i % 4 == 0:
            action = {
                'vector': kmeans.cluster_centers_[np.random.choice(32)]
            }
    
        obs, reward, done, info = env.step(action)
        env.render()
    
        if reward > 0:
            print("+{} reward!".format(reward))
        net_reward += reward
        i += 1
    
    print("Total reward: ", net_reward)


if __name__ == '__main__':
    main()




"""
logging.basicConfig(level=logging.DEBUG)

env = gym.make('MineRLNavigateDense-v0')
obs = env.reset()

done = False


rewards = []
compass = []
times = []
tic = time.perf_counter()
net_reward = 0
output_filename = "/Volumes/My Data/Minecraft AI/graphs/MineRLNavigateDense-v0"
while not done:
    action = env.action_space.noop()

    action['camera'] = [0, 0.03*obs["compassAngle"]]
    action['back'] = 0
    action['forward'] = 1
    action['jump'] = 1
    action['attack'] = 1

    obs, reward, done, info = env.step(
        action)

    net_reward += reward
    toc = time.perf_counter()
    times.append(str(toc - tic))
    rewards.append(net_reward)
    compass.append(obs['compassAngle'])
df = pd.DataFrame(list(zip(times, rewards)),
               columns =['Time', 'Reward'])
df2 = pd.DataFrame(list(zip(times, compass)),
               columns =['Time', 'Compass'])
fig1 = px.line(df, x="Time", y="Reward", title='Reward over Time')
fig2 = px.line(df2, x="Time", y="Compass", title='Compass over Time')

figures_to_html([fig1, fig2], filename = output_filename + ".html")"""