# -*- coding: utf-8 -*-
"""
Created on Sat May 17 21:37:49 2014

@author: Bas Rustenburg, Hyunwoo Cho

"""
import networkx as nx
import numpy as np
import tools
from tools import pairwise


def abcd():
    subway = nx.Graph()

    STATIONS = [tuple(['a', 0, 10, 0, 1]), tuple(['b', 10, 10, 0, 1]), tuple(['c', 20, 10, 0, 1]), tuple(['d', 30, 10, 0, 1])]

    stations = list()

    for S in STATIONS:
        stations.append(tools.BasicStation(*S))

    for s in stations:
        subway.add_node(s)

    lines = { '1': tools.Line('1',stations[0:4]),
            }

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)

    train1 = tools.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train2 = tools.Train('1-2', 30, lines['1'], stations[1], -1, 1.0, verbose=0)
    trains = [train1,train2]

    return subway,lines,stations,trains


def abcdefg():
    subway = nx.Graph()

    STATIONS = [tuple(['a', 0, 10, 0, 1]), tuple(['b', 10, 10, 0, 1]), tuple(['c', 20, 10, 0, 1]), tuple(['d', 30, 10, 0, 1]),tuple(['e', 20, 30, 0, 1]), tuple(['f', 20, 20, 0, 1]), tuple(['g', 20, 0, 0, 1])]

    stations = list()

    for S in STATIONS:
        stations.append(tools.BasicStation(*S))
    #
    for s in stations:
        subway.add_node(s)

    lines = { '1': tools.Line('1',stations[0:4]),
              '2': tools.Line('2', [stations[4],stations[5],stations[2],stations[6]] )}

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)


    train1 = tools.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train2 = tools.Train('1-2', 30, lines['1'], stations[1], 1, 1.0, verbose=0)
    train3 = tools.Train('1-3', 30, lines['1'], stations[2], 1, 1.0, verbose=0)
    train4 = tools.Train('1-4', 30, lines['1'], stations[3], 1, 1.0, verbose=1)
    train5 = tools.Train('1-1', 30, lines['1'], stations[0], -1, 1.0, verbose=0)
    train6 = tools.Train('1-2', 30, lines['1'], stations[1], -1, 1.0, verbose=0)
    train7 = tools.Train('1-3', 30, lines['1'], stations[2], -1, 1.0, verbose=0)
    train8 = tools.Train('1-4', 30, lines['1'], stations[3], -1, 1.0, verbose=0)

    trains = [train1,train2,train3,train4,train5,train6,train7,train8]

    return subway,lines,stations,trains

def labcdefg():
    subway = nx.Graph()

    STATIONS = [tuple(['a', 0, 10, 0, 1, ['1']]), tuple(['b', 10, 10, 0, 1, ['1']]), tuple(['c', 20, 10, 0, 1, ['1','2']]), tuple(['d', 30, 10, 0, 1, ['1']]),tuple(['e', 20, 30, 0, 1, ['2']]), tuple(['f', 20, 20, 0, 1, ['2']]), tuple(['g', 20, 0, 0, 1, ['2']])]

    stations = list()

    for S in STATIONS:
        stations.append(tools.LineStation(*S))

    for s in stations:
        subway.add_node(s)

    lines = { '1': tools.Line('1',stations[0:4]),
              '2': tools.Line('2', [stations[4],stations[5],stations[2],stations[6]] )}

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)


    train1 = tools.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train2 = tools.Train('1-2', 30, lines['1'], stations[1], 1, 1.0, verbose=0)
    train3 = tools.Train('1-3', 30, lines['1'], stations[2], 1, 1.0, verbose=0)
    train4 = tools.Train('1-4', 30, lines['1'], stations[3], 1, 1.0, verbose=1)


    trains = [train1,train2,train3,train4]



    return subway,lines,stations,trains

def labcdefghi():
    """
    This system has 4 lines.
    Line 1: a-b-c-d
    Line 2: e-f-c-g
    Line 3: f-i-b-h-g
    Line 4: a-c-e
    """
    subway = nx.Graph()

    STATIONS = [tuple(['a', 0, 10, 0, 1, ['1','4']]), tuple(['b', 10, 10, 0, 1, ['1','3']]), tuple(['c', 20, 10, 0, 1, ['1','2','4']]), tuple(['d', 30, 10, 0, 1, ['1']]),tuple(['e', 20, 30, 0, 1, ['2','4']]), tuple(['f', 20, 20, 0, 1, ['2','3']]), tuple(['g', 20, 0, 0, 1, ['2','3']]),tuple(['h', 10, 0, 0, 1, ['3']]),tuple(['i', 10, 20, 0, 1, ['3']])]
    stations = list()

    for S in STATIONS:
        stations.append(tools.LineStation(*S))

    for s in stations:
        subway.add_node(s)

    lines = { '1': tools.Line('1',stations[0:4]),
              '2': tools.Line('2', [stations[4],stations[5],stations[2],stations[6]]),
              '3': tools.Line('3', [stations[5],stations[8], stations[1],stations[7],stations[6]]),
              '4': tools.Line('4', [stations[0], stations[2], stations[4]])
              }

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)


    train11 = tools.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train12 = tools.Train('1-2', 30, lines['1'], stations[3], -1, 1.0, verbose=0)
    train21 = tools.Train('2-1', 30, lines['2'], stations[4], 1, 1.0, verbose=0)
    train22 = tools.Train('2-2', 30, lines['2'], stations[6], -1, 1.0, verbose=0)
    train31 = tools.Train('3-1', 30, lines['3'], stations[5], 1, 1.0, verbose=0)
    train32 = tools.Train('3-2', 30, lines['3'], stations[6], -1, 1.0, verbose=0)
    train41 = tools.Train('4-1', 30, lines['4'], stations[0], 1, 1.0, verbose=0)
    train42 = tools.Train('4-2', 30, lines['4'], stations[4], -1, 1.0, verbose=0)

    trains = [train11,train12,train21,train22,train31, train32,train41,train42]



    return subway,lines,stations,trains

def circle():
    """
    This system has 4 lines.
    Line 1: a-b-c-d
    Line 2: e-f-c-g
    Line 3: c-f-i-b-h-g
    Line 4: a-c-e
    """
    subway = nx.Graph()

    STATIONS = [tuple(['a', 0, 10, 0, 1, ['1','4']]), tuple(['b', 10, 10, 0, 1, ['1','3']]), tuple(['c', 20, 10, 0, 1, ['1','2','3','4']]), tuple(['d', 30, 10, 0, 1, ['1']]),tuple(['e', 20, 30, 0, 1, ['2','4']]), tuple(['f', 20, 20, 0, 1, ['2','3']]), tuple(['g', 20, 0, 0, 1, ['2','3']]),tuple(['h', 10, 0, 0, 1, ['3']]),tuple(['i', 10, 20, 0, 1, ['3']])]
    stations = list()

    for S in STATIONS:
        stations.append(tools.LineStation(*S))
    
    for s in stations:
        subway.add_node(s)

    lines = { '1': tools.Line('1',stations[0:4]),
              '2': tools.Line('2', [stations[4],stations[5],stations[2],stations[6]]),
              '3': tools.CircleLine('3', [stations[2], stations[5],stations[8], stations[1],stations[7],stations[6]]),
              '4': tools.Line('4', [stations[0], stations[2], stations[4]])
              }

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)


    train11 = tools.Train('1-1', 30, lines['1'], stations[0], 1, 1.0, verbose=0)
    train12 = tools.Train('1-2', 30, lines['1'], stations[3], -1, 1.0, verbose=0)
    train21 = tools.Train('2-1', 30, lines['2'], stations[4], 1, 1.0, verbose=0)
    train22 = tools.Train('2-2', 30, lines['2'], stations[2], -1, 1.0, verbose=0)
    train31 = tools.Train('3-1', 30, lines['3'], stations[2], 1, 1.0, verbose=0)
    train32 = tools.Train('3-2', 30, lines['3'], stations[6], -1, 1.0, verbose=1)
    train41 = tools.Train('4-1', 30, lines['4'], stations[0], 1, 1.0, verbose=0)
    train42 = tools.Train('4-2', 30, lines['4'], stations[4], -1, 1.0, verbose=0)

    trains = [train11,train12,train21,train22,train31, train32,train41,train42]



    return subway,lines,stations,trains



def nyc():
    subway = nx.Graph()
    STATIONS = []
    with open('../listOfStationsConverted.txt') as f:
        #skip header
        f.readline()
        rows = (line.strip().split("\t") for line in f)
        for row in rows:
            STATIONS.append(tuple([
            row[0],
            (int(row[5]) if (row[3][-2] == 'X') else int(row[5]) - 100000),
            (int(row[4]) if (row[3][-1] == 'L') else int(row[4]) - 100000),
            0,
            1,
            list(row[0].split(";")[-1])
            ]))

    stations = dict()
    
    for S in STATIONS:
        stations[S[0]] = tools.LineStation(*S)

    for s in stations.itervalues():
        subway.add_node(s)

    lines = dict()
    lines_information = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [],
                         '7': [], 'A': [], 'B': [], 'C': [], 'D': [], 'E': [],
                         'F': [], 'G': [], 'H': [], 'J': [], 'L': [], 'M': [],
                         'N': [], 'Q': [], 'R': [], 'S': [], 's': [], 'Z': []}

    with open('../listOfLines.txt') as f:
        rows = (line.strip().split("\t") for line in f)
        for row in rows:
            lines_information[row[0]] = row[1:]

# new line
    #lines_information['8'] = [';4567S', ';7BDFM', ';1237ACENQRS', '34th St;ACE',
    #                          '34th St;123', ';BDFMNQR', '33rd St;6', '28th St;6',
    #                          '23rd St;6', ';456LNQR', ';123FLM', ';ACEL',
    #                          '23rd St;CE', '34th St;ACE', '34th St;123', ';BDFMNQR',
    #                          '33rd St;6']
# block line
    #del lines_information['R']

    for key, value in lines_information.iteritems():
        stations_list = []
        for j in value:
            stations_list.append(stations[j])
        if key == '8':
            lines[key] = tools.CircleLine(key, stations_list)
        else:
            lines[key] = tools.Line(key, stations_list)

    for l in lines.values():
        for pair in pairwise(l.route):
            dist = np.linalg.norm([pair[0].xy,pair[1].xy])
            subway.add_edge(*pair, distance=dist)

    trains = []
    for key in lines_information.iterkeys():
        serial = 1
        for j in range(0, len(lines_information[key]), 5):
            trains.append(tools.Train(name=key + '-' + str(serial),
                                      capacity=30,
                                      line=lines[key],
                                      start=stations[lines_information[key][j]],
                                      direction=1, velocity=100.0,
                                      verbose=0))
            serial += 1
        if (len(lines_information[key]) - 1 % 5 == 0):
            trains.pop()
        for j in range(len(lines_information[key]) - 1, 0, -5):
            trains.append(tools.Train(name=key + '-' + str(serial),
                                      capacity=30,
                                      line=lines[key],
                                      start=stations[lines_information[key][j]],
                                      direction=1, velocity=100.0,
                                      verbose=0))
            serial += 1

    return subway,lines,stations,trains
