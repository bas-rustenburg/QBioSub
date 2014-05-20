# -*- coding: utf-8 -*-
"""
Created on Mon May 19 19:48:40 2014

@author: rustenburg
"""

import systems,objects,functions,visualization

subway,lines,stations,trains = systems.labcdefghi()
visualization.subway_map(subway,"labcdefghi.png")

pathmatrix = functions.generate_all_routes(subway)
distmatrix = functions.dist_transf(pathmatrix)

for x in distmatrix.iteritems():
    print "PAIR"
    print x