# -*- coding: utf-8 -*-
"""
Created on Sun May 25 17:28:13 2014

@author: rustenburg
"""

import line_connectivity, tools, systems
import pickle

subway,lines,stations,trains = systems.nyc()

#for x in range(100):
#    test = tools.lines_first_search(stations.popitem()[1],stations.popitem()[1], lines,line_connectivity.linegraph,offset=1)
sm = tools.line_first_travel_instructions(stations,lines,line_connectivity.linegraph,offset=1)

pickle.dump(sm, "offset_1.p")

no_offset = tools.line_first_travel_instructions(stations,lines,line_connectivity.linegraph,offset=0)

pickle.dump(no_offset, "offset_0.p")
