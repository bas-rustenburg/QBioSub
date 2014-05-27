# -*- coding: utf-8 -*-
"""
Created on Mon May 26 18:30:02 2014

@author: rustenburg
"""

from derailed import line_connectivity, tools, systems
import pickle


subway,lines,stations,trains = systems.nyc()

off1 = open("offset_1.p", "wb")
p = pickle.Pickler(off1)


instructions = tools.line_first_travel_instructions(stations,lines,line_connectivity.linegraph,offset=1)
dataset = tuple([instructions,subway,lines,stations,trains])

p.dump(dataset)

off1.close()
