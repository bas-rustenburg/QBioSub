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
up = pickle.Unpickler(pickled_system)
instructions,subway,lines,stations,trains= up.load()
pickled_system.close()

timesteps = 2
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=stations.values(),instructions=instructions) for station in stations.itervalues()]
    [train.update() for train in trains]
 

print "dun"
