# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:12:12 2014

@author: rustenburg
"""

import tools
from systems import nyc

import matplotlib.pyplot as plt
import networkx as nx

subway,lines,stations,trains = nyc(add=False, block="none")
subway8,lines8,stations8,trains8 = nyc(add=True, block="none")
subwayR,linesR,stationsR,trainsR = nyc(add=False, block="all")
subwaynqr,linesnqr,stationsnqr,trainsnqr = nyc(add=False, block="manhattan")

degree_sequence=sorted(nx.degree(subway).values(),reverse=True)
dmax=max(degree_sequence)
degree_sequence8=sorted(nx.degree(subway8).values(),reverse=True)
dmax8=max(degree_sequence8)
degree_sequenceR=sorted(nx.degree(subwayR).values(),reverse=True)
dmaxR=max(degree_sequenceR)
degree_sequencenqr=sorted(nx.degree(subwaynqr).values(),reverse=True)
dmaxnqr=max(degree_sequencenqr)

Gcc=nx.connected_component_subgraphs(subway)[0]
pos=nx.spring_layout(Gcc)
Gcc8=nx.connected_component_subgraphs(subway8)[0]
pos8=nx.spring_layout(Gcc8)
GccR=nx.connected_component_subgraphs(subwayR)[0]
posR=nx.spring_layout(GccR)
Gccnqr=nx.connected_component_subgraphs(subwaynqr)[0]
posnqr=nx.spring_layout(Gccnqr)

plt.axes([0.1, 0.4, 0.85, 0.55])
plt.loglog(degree_sequence,'k-',marker='')
plt.loglog(degree_sequence8, 'r--', marker='')
plt.loglog(degree_sequenceR, 'g--', marker='')
plt.loglog(degree_sequencenqr, 'b--', marker='')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.axes([0,0,0.25,0.25])
plt.axis('off')
nx.draw_networkx_nodes(Gcc,pos,node_size=16, node_color='0.75')
nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
plt.title("Original")
plt.axes([0.25,0,0.25,0.25])
plt.axis('off')
nx.draw_networkx_nodes(Gcc8,pos8,node_size=16, node_color='r')
nx.draw_networkx_edges(Gcc8,pos8,alpha=0.4)
plt.title("Line '8' added")
plt.axes([0.5,0,0.25,0.25])
plt.axis('off')
nx.draw_networkx_nodes(GccR,posR,node_size=16, node_color='g')
nx.draw_networkx_edges(GccR,posR,alpha=0.4)
plt.title("Line R removed")
plt.axes([0.75,0,0.25,0.25])
plt.axis('off')
nx.draw_networkx_nodes(Gccnqr,posnqr,node_size=16, node_color='b')
nx.draw_networkx_edges(Gccnqr,posnqr,alpha=0.4)
plt.title("N, Q, R in Manhattan removed", size=9)
plt.savefig("degree_histogram.png")

nx.average_clustering(Gcc)
nx.average_clustering(Gcc8)
nx.average_clustering(GccR)
nx.average_clustering(Gccnqr)

between = {}
between8 = {}
betweenR = {}
betweennqr = {}
for key, value in nx.betweenness_centrality(Gcc).iteritems():
    between[key.name] = value

for key, value in nx.betweenness_centrality(Gcc8).iteritems():
    between8[key.name] = value

for key, value in nx.betweenness_centrality(GccR).iteritems():
    betweenR[key.name] = value

for key, value in nx.betweenness_centrality(Gccnqr).iteritems():
    betweennqr[key.name] = value

sorted(between, key=between.get)[-20:]
sorted(between8, key=between8.get)[-20:]
sorted(betweenR, key=betweenR.get)[-20:]
sorted(betweennqr, key=betweennqr.get)[-20:]

#tools.travel_instructions(subway,lines,order=["transfers","stops","distance"], cutoff = 70)