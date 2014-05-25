# -*- coding: utf-8 -*-
"""
Created on Sun May 25 15:04:06 2014

@author: rustenburg
"""
import networkx as nx

linegraph = nx.Graph()

line= ['1','2','3','4','5','6','7','A','B','C',
        'D','E','F','G','H','J','L','M','N','Q',
        'R','S','s','Z']

line1 = ["1","2","3","7","A","B","C","D","E","F","L","M","N","Q","R","S"]
line2 = ["1","2","3","4","5","7","A","B","C","D","E","F","J","L","M","N","Q","R","s","S","Z"]
line3 = ["1","2","3","4","5","7","A","B","C","D","E","F","J","L","M","N","Q","R","s","S","Z"]
line4 = ["2","3","4","5","6","7","A","B","C","D","J","L","N","Q","R","s","S","Z"]
line5 = ["2","3","4","5","6","7","A","B","C","D","J","L","N","Q","R","s","S","Z"]
line6 = ["4","5","6","7","B","D","E","F","J","L","M","N","Q","R","S","Z"]
line7 = ["1","2","3","4","5","6","7","A","B","C","D","E","F","G","M","N","Q","R","S"]
lineA = ["1","2","3","4","5","7","A","B","C","D","E","F","G","H","J","L","M","N","Q","R","S","Z"]
lineB = ["1","2","3","4","5","6","7","A","B","C","D","E","F","M","N","Q","R","s"]
lineC = ["1","2","3","4","5","7","A","B","C","D","E","F","G","J","L","M","N","Q","R","s","S","Z"]
lineD = ["1","2","3","4","5","6","7","A","B","C","D","E","F","M","N","Q","R"]
lineE = ["1","2","3","6","7","A","B","C","D","E","F","G","J","L","M","N","Q","R","S","Z"]
lineF = ["1","2","3","6","7","A","B","C","D","E","F","G","J","L","M","N","Q","R","Z"]
lineG = ["7","A","C","E","F","G","L","M","R"]
lineJ = ["2","3","4","5","6","A","C","E","F","J","L","M","N","Q","R","Z"]
lineL = ["1","2","3","4","5","6","A","C","E","F","G","J","L","M","N","Q","R","Z"]
lineM = ["1","2","3","6","7","A","B","C","D","E","F","G","J","L","M","N","Q","R","Z"]
lineN = ["1","2","3","4","5","6","7","A","B","C","D","E","F","J","L","M","N","Q","R","S","Z"]
lineQ = ["1","2","3","4","5","6","7","A","B","C","D","E","F","J","L","M","N","Q","R","s","S","Z"]
lineR = ["1","2","3","4","5","6","7","A","B","C","D","E","F","G","J","L","M","N","Q","R","S","Z"]
lineZ = ["2","3","4","5","6","A","C","E","F","J","L","M","N","Q","R","Z"]
lineS = ["1","2","3","4","5","6","7","A","C","E","N","Q","R","S"]
lines = ["2","3","4","5","B","C","Q","s"]
lineH = ["A","H"]

lineconnections={'1' : line1,
                 '2' : line2,
                 '3' : line3,
                 '4' : line4,
                 '5' : line5,
                 '6' : line6,
                 '7' : line7,
                 'A' : lineA,
                 'B' : lineB,
                 'C' : lineC,
                 'D' : lineD,
                 'E' : lineE,
                 'F' : lineF,
                 'G' : lineG,
                 'H' : lineH,
                 'J' : lineJ,
                 'L' : lineL,
                 'M' : lineM,
                 'N' : lineN,
                 'Q' : lineQ,
                 'R' : lineR,
                 'S' : lineS,
                 's' : lines,
                 'Z' : lineZ
                }



linegraph.add_nodes_from(line)
node_colors=["#EE352E","#EE352E","#EE352E","#00933C","#00933C",
             "#00933C","#B933AD","#2850AD","#FF6319","#2850AD",
             "#FF6319","#2850AD","#FF6319","#6CBE45","#808183",
             "#996633","#A7A9AC","#FF6319","#FCCC0A","#FCCC0A",
             "#FCCC0A","#808183","#808183","#996633"]

for key,val in lineconnections.iteritems():
    for connection in val:
        linegraph.add_edge(key,connection)

from matplotlib import pyplot as plt

plt.figure(dpi=300)
#plt.axes(frameon=False)
plt.axis('off')


nx.draw_spring(linegraph,nodelist=line,node_color=node_colors)

nx.write_gexf(linegraph, "./Lines_Connectivity.gexf")
             
#linegraph.add_edges