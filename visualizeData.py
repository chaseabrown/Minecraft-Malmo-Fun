#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:21:07 2021

@author: chasebrown
"""

import gym
import minerl
import logging
import pandas as pd
import numpy as np
import time
import PIL
import os

os.environ["JAVA_HOME"] = "/Users/chasebrown/opt/anaconda3/envs/minerl38"

def get_concat_h_cut(im1, im2):
    dst = PIL.Image.new('RGB', (im1.width + im2.width, min(im1.height, im2.height)))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v_cut(im1, im2):
    dst = PIL.Image.new('RGB', (min(im1.width, im2.width), im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def main():
    logging.basicConfig(level=logging.DEBUG)
    
    env = gym.make('MineRLNavigateDense-v0')
    obs = env.reset()
    
    done = False
    
    
    net_reward = 0
    while not done:
        action = env.action_space.noop()
    
        action['camera'] = [0, 0.03*obs["compassAngle"]]
        action['back'] = 0
        action['forward'] = 1
        action['jump'] = 1
        action['attack'] = 1
    
        obs, reward, done, info = env.step(action)
        #env.render()
        pov = obs['pov']
        """im1 = PIL.Image.fromarray(pov[0][0], "RGB")
        for i in range(1,32):
            pov3 = pov[0][i]
            im2 = PIL.Image.fromarray(pov3, "RGB")
            im1 = get_concat_h_cut(im1, im2)
        for s in range(1,16):
            im3 = PIL.Image.fromarray(pov[s][0], "RGB")
            for i in range(1,32):
                pov3 = pov[s][i]
                im4 = PIL.Image.fromarray(pov3, "RGB")
                im3 = get_concat_h_cut(im3, im4)
            im1 = get_concat_v_cut(im1, im3)
        im1.save("/Volumes/My Data/Minecraft AI/test.jpg")"""
    
        net_reward += reward
        time.sleep(30)
    


if __name__ == '__main__':
    main()
