# -*- coding: utf-8 -*-
"""
Created on Sun May 25 17:28:13 2014

@author: rustenburg
"""

import line_connectivity, tools, systems
subway,lines,stations,trains = systems.nyc()

sm = tools.line_first_travel_instructions(stations,lines,line_connectivity.linegraph,offset=1)