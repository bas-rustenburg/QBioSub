# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:23:56 2014

@author: Bas Rustenburg, Hyunwoo Choo
"""

#import networkx as nx
#import matplotlib
import random
import itertools
import visualization
import tools

from systems import abcd as simulation

random.seed(42)
print [random.randint(0,255),random.randint(0,255),random.randint(0,255)]


subway,lines,stations,trains = simulation()

#visualization.subway_map(subway)

pastotals = list()

timesteps = 140
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=stations) for station in stations]
    [train.update() for train in trains]
    pastotals.append(tools.Passenger.total)

visualization.subway_map(subway)



