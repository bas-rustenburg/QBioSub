# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:23:56 2014

@author: Bas Rustenburg, Hyunwoo Choo
"""

#import networkx as nx
#import matplotlib
import random
import itertools
import tools

from systems import labcdefghi as simulation

random.seed(42)
print [random.randint(0,255),random.randint(0,255),random.randint(0,255)]


subway,lines,stations,trains = simulation()
instructions=tools.travel_instructions(subway,lines)
#visualization.subway_map(subway)

pastotals = list()

timesteps = 1400
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=stations,instructions=instructions) for station in stations]
    [train.update() for train in trains]
    try:
        pastotals.append(tools.Passenger.total)
    except AttributeError:
        pastotals.append(0)


import matplotlib.pyplot as plt

#Get rid of passengers
for t in trains:
    del(t.passengers)

for s in stations:
    del(s.passengers)

plt.figure()
plt.xlabel("Timesteps")
plt.ylabel("Passengers")
plt.plot(pastotals)
plt.figure()
plt.xlabel("Passengers")
plt.ylabel("Lifetime (timesteps)")
x = tools.Passenger.lifetimes

y= list()
for z in x:
    if z > 200:
        y.append(z)
        
plt.plot(y)



