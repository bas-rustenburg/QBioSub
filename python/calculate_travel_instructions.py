# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:12:12 2014

@author: rustenburg
"""

import tools
from systems import nyc

import matplotlib.pyplot as plt
import networkx as nx

subway,lines,stations,trains = nyc(add=False, block=True)

degree_sequence=sorted(nx.degree(subway).values(),reverse=True)
dmax=max(degree_sequence)
plt.loglog(degree_sequence,'b-',marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.axes([0.55,0.55,0.38,0.38])
Gcc=nx.connected_component_subgraphs(subway)[0]
pos=nx.spring_layout(Gcc)
plt.axis('off')
nx.draw_networkx_nodes(Gcc,pos,node_size=16)
nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
plt.savefig("degree_histogram_line_R.png")


#tools.travel_instructions(subway,lines,order=["transfers","stops","distance"], cutoff = 70)