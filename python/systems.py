# -*- coding: utf-8 -*-
"""
Created on Sat May 17 21:37:49 2014

@author: Bas Rustenburg, Hyunwoo Cho

"""
import networkx as nx
import objects


from matplotlib import pylab
import matplotlib.pyplot as plt

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,) #bbox_inches="tight"
    pylab.close()
    del fig





def pairwise(sequence):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    pairs=list()
    for i in range(len(sequence)-1):
        pairs.append(tuple([sequence[i],sequence[i+1]]))
        
    return pairs



  

def abcd():
    subway = nx.Graph()    
    
    STATIONS = [tuple(['a', 0, 10, 0, 1]), tuple(['b', 10, 10, 0, 1]), tuple(['c', 20, 10, 0, 1]), tuple(['d', 30, 10, 0, 1]),tuple(['e', 20, 30, 0, 1]), tuple(['f', 20, 20, 0, 1]), tuple(['g', 20, 0, 0, 1])]

    stations = list()

    for S in STATIONS:
        stations.append(objects.BasicStation(*S))
    #
    for s in stations:
        subway.add_node(s)
    
      
    lines = { '1': objects.Line('1',stations[0:4]),
              '2': objects.Line('2', [stations[4],stations[5],stations[2],stations[6]] )}
    
    
    for l in lines.values():
        subway.add_edges_from(pairwise(l.route))
    save_graph(subway,"my_graph.pdf")     
        
    train1 = objects.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train2 = objects.Train('1-2', 30, lines['1'], stations[1], 1, 1.0, verbose=0)
    train3 = objects.Train('1-3', 30, lines['1'], stations[2], 1, 1.0, verbose=0)
    train4 = objects.Train('1-4', 30, lines['1'], stations[3], 1, 1.0, verbose=1)
    train5 = objects.Train('1-1', 30, lines['1'], stations[0], -1, 1.0, verbose=0)
    train6 = objects.Train('1-2', 30, lines['1'], stations[1], -1, 1.0, verbose=0)
    train7 = objects.Train('1-3', 30, lines['1'], stations[2], -1, 1.0, verbose=0)
    train8 = objects.Train('1-4', 30, lines['1'], stations[3], -1, 1.0, verbose=0)
    
    trains = [train1,train2,train3,train4,train5,train6,train7,train8]
    
    return stations,trains,lines