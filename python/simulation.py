# -*- coding: utf-8 -*-
"""
Created on Wed May 14 16:23:56 2014

@author: Bas Rustenburg, Hyunwoo Cho
"""

import random
import itertools
import pickle
import derailed.tools as tools

random.seed(47)
#print [random.randint(0,255),random.randint(0,255),random.randint(0,255)]

pickled_system = open("offset_1.p", "rb") # Open pickled file object
up = pickle.Unpickler(pickled_system)
instructions,subway,lines,stations,trains= up.load()
pickled_system.close()

passengerlogs = open("pas_totals.log", "w")

count = 0
timesteps = 200000
for _ in itertools.repeat(None,timesteps):
    [station.update(destinations=stations.values(),instructions=instructions) for station in stations.itervalues()]
    [train.update() for train in trains]
    passengerlogs.write("%s\n"%(tools.Passenger.total))
    count += 1 
    print count
 
passengerlogs.close()