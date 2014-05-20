# -*- coding: utf-8 -*-
"""
Created on Mon May 19 18:42:14 2014

@author: Bas Rustenburg, Hyunwoo Cho
"""

import objects
import networkx as nx
import numpy as np

def pairwise(sequence):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    pairs=list()
    for i in range(len(sequence)-1):
        pairs.append(tuple([sequence[i],sequence[i+1]]))

    return pairs

def generate_all_routes(graph):
    """
    Generate all routes for a passenger to take through the subway that only pass a station once
    """
    pathmatrix = dict()   
    for outer in graph.nodes_iter():
        for inner in graph.nodes_iter():
                pathmatrix[tuple([outer,inner])] = list(nx.all_simple_paths(graph,outer,inner))
    return pathmatrix

def dist_transf(pathmatrix):
    """
    calculate the distances belonging to a set of paths and the line along the route
    """
    pmx = pathmatrix
    dmatrix = dict()
    for key,paths in pmx.iteritems():
        dists=list()
        lines=list()
        for path in paths:
            dist = np.float64()
            line = list()
            for stationa,stationb in pairwise(path):
                dist += np.linalg.norm([stationa.xy,stationb.xy])
                line.append(np.intersect1d(stationa.lines,stationb.lines))
            dists.append(dist)
            lines.append(line)
        dmatrix[key]=zip(paths,lines,dists)
    #dmatrix contains station pairs as keys, points to possible paths, with lines taken along paths, and total distance of the path
    #Example:    
    #dmatrix[a,d] => ([[a,b,c,d],...], ['1','1','1'], 82.09) 
    return dmatrix
    

