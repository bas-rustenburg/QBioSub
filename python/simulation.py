# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:23:56 2014

@author: Bas Rustenburg, Hyunwoo Cho
"""

#import networkx as nx
#import matplotlib
import random
import itertools
import pickle


#from systems import labcdefghi as simulation
from systems import nyc as simulation

random.seed(47)
print [random.randint(0,255),random.randint(0,255),random.randint(0,255)]


subway,lines,stations,trains = simulation()

pickled_instructions = open("offset_1.p", "rb") # Open pickled file object



instructions= pickle.load(pickled_instructions)

pickled_instructions.close()




#visualization.subway_map(subway)

pastotals = list()

timesteps = 0
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=stations,instructions=instructions) for station in stations]
    [train.update() for train in trains]
 

