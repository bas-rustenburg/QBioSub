# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:23:56 2014

@author: B-Rus and Hy-C
"""

#import networkx as nx
#import matplotlib
import random
import objects
import itertools
import numpy as np


random.seed(1987)
print random.randint(0,250)


STATIONS = [tuple(['a', 0, 10, 0, 2]), tuple(['b', 10, 20, 0, 2]), tuple(['c', 20, 10, 0, 2]), tuple(['d', 10, 0, 0, 2])]

statlist = set()

for s in STATIONS:
    statlist.add(objects.BasicStation(*s))
#    
line = objects.Line('1',list(random.sample(statlist,4)))

    
train1 = objects.Train('1-1', 30, line, random.sample(statlist,1)[0], 1, 1.0, verbose=1)
train2 = objects.Train('1-2', 30, line, random.sample(statlist,1)[0], -1, 1.0, verbose=1)

trains = [train1,train2]
timesteps = 500
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=statlist) for station in statlist]
    [train.update() for train in trains]

