# -*- coding: utf-8 -*-
"""
Created on Mon May 19 19:48:40 2014

@author: rustenburg
"""

import systems,objects,functions,visualization

subway,lines,stations,trains = systems.abcdefg()
pathmatrix = functions.generate_all_routes(subway)
distmatrix = functions.calculate_distances(pathmatrix)