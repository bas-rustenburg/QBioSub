# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:12:12 2014

@author: rustenburg
"""

import tools
from systems import nyc

import matplotlib.pyplot as plt
import networkx as nx

subway,lines,stations,trains = nyc(add=False, block=False)
subway8,lines8,stations8,trains8 = nyc(add=True, block=False)
subwayR,linesR,stationsR,trainsR = nyc(add=False, block=True)

degree_sequence=sorted(nx.degree(subway).values(),reverse=True)
dmax=max(degree_sequence)
degree_sequence8=sorted(nx.degree(subway8).values(),reverse=True)
dmax8=max(degree_sequence8)
degree_sequenceR=sorted(nx.degree(subwayR).values(),reverse=True)
dmaxR=max(degree_sequenceR)
plt.axes([0.1, 0.45, 0.85, 0.5])
plt.loglog(degree_sequence,'k-',marker='o')
plt.loglog(degree_sequence8, 'b-', marker='^')
plt.loglog(degree_sequenceR, 'm-', marker='s')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.axes([0,0,0.3,0.3])
Gcc=nx.connected_component_subgraphs(subway)[0]
pos=nx.spring_layout(Gcc)
plt.axis('off')
nx.draw_networkx_nodes(Gcc,pos,node_size=16)
nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
plt.title("Original")
plt.axes([0.3,0,0.3,0.3])
Gcc8=nx.connected_component_subgraphs(subway8)[0]
pos8=nx.spring_layout(Gcc8)
plt.axis('off')
nx.draw_networkx_nodes(Gcc8,pos8,node_size=16)
nx.draw_networkx_edges(Gcc8,pos8,alpha=0.4)
plt.title("Line '8' added")
plt.axes([0.6,0,0.3,0.3])
GccR=nx.connected_component_subgraphs(subwayR)[0]
posR=nx.spring_layout(GccR)
plt.axis('off')
nx.draw_networkx_nodes(GccR,posR,node_size=16)
nx.draw_networkx_edges(GccR,posR,alpha=0.4)
plt.title("Line R removed")
plt.savefig("degree_histogram.png")


#tools.travel_instructions(subway,lines,order=["transfers","stops","distance"], cutoff = 70)