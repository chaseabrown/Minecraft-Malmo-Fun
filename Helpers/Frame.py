#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 20:49:53 2021

@author: chasebrown
"""

import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import numpy as np
import random
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class Frame:
    
    def __init__(self):
        self.state_size = state_size
        self.action_size = action_size
        
        #Used for sampling from past experiences. This is important for making sure there is enough variety in the actions
        self.memory = deque(maxlen=2000)
        
        self.gamma = 0.95
        
        #Helps balance exploitation vs exploration
        self.epsilon = 1.0
        self.epsilon_decay = 0.9995
        self.epsilon_min = 0.01
        
        #Step size for our optimizer
        self.learning_rate = 0.001
        
        self.model = self._build_model()
        
    def _build_model(self):
        
        # Set up Model
        model = Sequential()
        
        # Hidden Layers
        model.add(Dense(24, input_dim = self.state_size, activation='relu'))
        model.add(Dense(48, activation = 'relu'))
        model.add(Dense(96, activation = 'relu'))
        model.add(Dense(48, activation = 'relu'))
        model.add(Dense(24, activation = 'relu'))

        
        # Output Layer
        model.add(Dense(self.action_size, activation='linear'))
        
        #Compile Model
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        
        return model
    
    #Create Datapoint for learning
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    #Determine explore or exploit
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    #Uses batch of memories to train the model
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            
            self.model.fit(state, target_f, epochs=1, verbose=0)
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    #Load model
    def load(self,name):
        self.model.load_weights(name)
    
    #Save Model
    def save(self, name):
        self.model.save_weights(name)