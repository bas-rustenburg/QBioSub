# -*- coding: utf-8 -*-
"""
Created on Mon May 19 19:48:40 2014

@author: rustenburg
"""

import systems,tools

subway,lines,stations,trains = systems.labcdefghi()
tools.subway_map(subway,"labcdefghi.png")

pathmatrix = tools.generate_all_routes(subway)
distmatrix = tools.dist_transf(pathmatrix)

for x in distmatrix.iteritems():
    print "PAIR"
    print x