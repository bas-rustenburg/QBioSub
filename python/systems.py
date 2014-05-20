# -*- coding: utf-8 -*-
"""
Created on Sat May 17 21:37:49 2014

@author: Bas Rustenburg, Hyunwoo Cho

"""
import networkx as nx
import numpy as np
import objects
from functions import pairwise


def abcd():
    subway = nx.Graph()

    STATIONS = [tuple(['a', 0, 10, 0, 1]), tuple(['b', 10, 10, 0, 1]), tuple(['c', 20, 10, 0, 1]), tuple(['d', 30, 10, 0, 1])]

    stations = list()

    for S in STATIONS:
        stations.append(objects.BasicStation(*S))

    for s in stations:
        subway.add_node(s)

    lines = { '1': objects.Line('1',stations[0:4]),
            }

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)

    train1 = objects.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train2 = objects.Train('1-2', 30, lines['1'], stations[1], -1, 1.0, verbose=0)
    trains = [train1,train2]

    return subway,lines,stations,trains


def abcdefg():
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
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)


    train1 = objects.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train2 = objects.Train('1-2', 30, lines['1'], stations[1], 1, 1.0, verbose=0)
    train3 = objects.Train('1-3', 30, lines['1'], stations[2], 1, 1.0, verbose=0)
    train4 = objects.Train('1-4', 30, lines['1'], stations[3], 1, 1.0, verbose=1)
    train5 = objects.Train('1-1', 30, lines['1'], stations[0], -1, 1.0, verbose=0)
    train6 = objects.Train('1-2', 30, lines['1'], stations[1], -1, 1.0, verbose=0)
    train7 = objects.Train('1-3', 30, lines['1'], stations[2], -1, 1.0, verbose=0)
    train8 = objects.Train('1-4', 30, lines['1'], stations[3], -1, 1.0, verbose=0)

    trains = [train1,train2,train3,train4,train5,train6,train7,train8]
    
    return subway,lines,stations,trains
    
def labcdefg():
    subway = nx.Graph()

    STATIONS = [tuple(['a', 0, 10, 0, 1, ['1']]), tuple(['b', 10, 10, 0, 1, ['1']]), tuple(['c', 20, 10, 0, 1, ['1','2']]), tuple(['d', 30, 10, 0, 1, ['1']]),tuple(['e', 20, 30, 0, 1, ['2']]), tuple(['f', 20, 20, 0, 1, ['2']]), tuple(['g', 20, 0, 0, 1, ['2']])]

    stations = list()

    for S in STATIONS:
        print S
        stations.append(objects.LineStation(*S))
    #
    for s in stations:
        subway.add_node(s)

    lines = { '1': objects.Line('1',stations[0:4]),
              '2': objects.Line('2', [stations[4],stations[5],stations[2],stations[6]] )}

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)


    train1 = objects.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train2 = objects.Train('1-2', 30, lines['1'], stations[1], 1, 1.0, verbose=0)
    train3 = objects.Train('1-3', 30, lines['1'], stations[2], 1, 1.0, verbose=0)
    train4 = objects.Train('1-4', 30, lines['1'], stations[3], 1, 1.0, verbose=1)
    train5 = objects.Train('1-1', 30, lines['1'], stations[0], -1, 1.0, verbose=0)
    train6 = objects.Train('1-2', 30, lines['1'], stations[1], -1, 1.0, verbose=0)
    train7 = objects.Train('1-3', 30, lines['1'], stations[2], -1, 1.0, verbose=0)
    train8 = objects.Train('1-4', 30, lines['1'], stations[3], -1, 1.0, verbose=0)

    trains = [train1,train2,train3,train4,train5,train6,train7,train8]
    
    

    return subway,lines,stations,trains