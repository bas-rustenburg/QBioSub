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


random.seed(42)
print random.randint(0,250)


STATIONS = [tuple(['a', 0, 10, 0, 0]), tuple(['b', 10, 20, 0, 0]), tuple(['c', 20, 10, 0, 0]), tuple(['d', 10, 0, 0, 1])]

statlist = list()

for s in STATIONS:
    statlist.append(objects.BasicStation(*s))
#    
line = objects.Line('1',statlist)

    
train1 = objects.Train('1-1', 30, line, statlist[0], 1, 1.0, verbose=3)
train2 = objects.Train('1-2', 30, line, statlist[1], 1, 1.0, verbose=3)
train3 = objects.Train('1-3', 30, line, statlist[2], 1, 1.0, verbose=3)
train4 = objects.Train('1-4', 30, line, statlist[3], 1, 1.0, verbose=3)

trains = [train1,train2,train3,train4]
timesteps = 30
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=statlist) for station in statlist]
    [train.update() for train in trains]
    print "Total: %s"%objects.Passenger.total
    

