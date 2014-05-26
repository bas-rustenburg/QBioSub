# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:23:56 2014

@author: Bas Rustenburg, Hyunwoo Cho
"""

import random
import itertools
import pickle

random.seed(47)
#print [random.randint(0,255),random.randint(0,255),random.randint(0,255)]

pickled_system = open("offset_1.p", "rb") # Open pickled file object
instructions,subway,lines,stations,trains= pickle.load(pickled_system)
pickled_system.close()

timesteps = 0
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=stations,instructions=instructions) for station in stations]
    [train.update() for train in trains]
 

