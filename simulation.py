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


random.seed(1989)
print random.randint(0,250)


STATIONS = [tuple(['a', 0, 1, 0, 24]), tuple(['b', 1, 2, 0, 24]), tuple(['c', 2, 1, 0, 24]), tuple(['d', 1, 0, 0, 24])]

statlist = set()

for s in STATIONS:
    statlist.add(objects.KillerStation(*s))
#    
timesteps = 14400
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=statlist) for station in statlist]


#x = objects.Train("F", [np.float64(0.0),np.float64(1.0)])  

