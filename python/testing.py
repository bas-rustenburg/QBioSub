# -*- coding: utf-8 -*-
"""
Created on Mon May 19 19:48:40 2014

@author: rustenburg
"""

import systems,tools

subway,lines,stations,trains = systems.labcdefghi()
    
pathmatrix = tools.generate_all_routes(subway)
distmatrix = tools.generate_dist_line(pathmatrix)
transmatrix = tools.solve_transfers(distmatrix,lines)

