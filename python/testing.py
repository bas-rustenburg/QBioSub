# -*- coding: utf-8 -*-
"""
Created on Mon May 19 19:48:40 2014

@author: rustenburg
"""

import systems,tools

subway,lines,stations,trains = systems.labcdefghi()
tools.subway_map(subway)    
instructions = tools.travel_instructions(subway,lines,order=["transfers","stops","distance"])

