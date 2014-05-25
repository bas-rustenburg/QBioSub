# -*- coding: utf-8 -*-
"""
Created on Sun May 25 17:28:13 2014

@author: rustenburg
"""

import line_connectivity, tools, systems
import numpy as np
import networkx as nx

subway,lines,stations,trains = systems.nyc()
least_transfers = tools.shortest_transfer(stations[';ACJLZ'], stations[';123FLM'],line_connectivity.linegraph)
unique_lines = tools.reduce_to_uniques(least_transfers)

reduced_lines = dict()
reduced_subway = nx.Graph()


for line in unique_lines:
    reduced_lines[line] = lines[line]

for l in reduced_lines.values():
        for pair in tools.pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            reduced_subway.add_edge(*pair, distance=dist)


tools.nyc_map(reduced_subway)
tools.nyc_map(subway,file_name="NYC.png")
