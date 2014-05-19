# -*- coding: utf-8 -*-
"""
Created on Mon May 19 14:59:47 2014

@author: Bas Rustenburg, Hyunwoo Cho
"""

import matplotlib.pyplot as plt
import networkx as nx

def subway_map(graph,file_name=None):
    """Visually represent the subway network and save to file"""
    # Turn interactive plotting off
    plt.ioff()
    positions = dict()
    labels = dict()
    for node in graph.nodes_iter():
        positions[node] = node.xy
        labels[node] = node.name
    plt.figure()
    nx.draw_networkx(graph,positions,labels=labels,node_size=200,node_color='chartreuse')
    if file_name:    
        plt.savefig(file_name, dpi=300)
    else: plt.show()
