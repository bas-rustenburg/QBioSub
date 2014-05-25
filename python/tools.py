# -*- coding: utf-8 -*-
"""
Created on Tue May 13 18:13:26 2014

@author: Bas Rustenburg, Hyunwoo Cho
"""

import random
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



#Global variable for debugging pathway solutions.
#Will capture any inconsistent paths for manual inspection when running consistent_resolver
weirdpaths=list()

#Some lists to throw at the consistent_resolver for debugging
xlist = [{1,2}, {1,2}, {2}, {2}, {3}]
vlist = xlist[::-1]
ylist = [{1,4,3},{2,4,3},{1,2,3},{2},{3},{3,2}]
zlist = ylist[::-1]
alist = [{1,2,5}, {1,2}, {1,2,4} ]
blist = alist[::-1]


#CLASSES#####################################################################


class Station(object):
    """
    Create a station.

    Parameters
    ----------
    name : string
        Identifier for this station.
    x : float
        x-coordinate for this station.
    y : float
        y-coordinate for this station.

    Attributes
    ----------
    name : string
        Identifier for this station.
    passengers : numpy.array
        Array of Passenger objects that are at current station
    xy : numpy.array([float,float])
        Pair of x,y coordinates to specify stations location.


    """
    def __init__(self,name,x,y):
        """
        Parameters
        ----------
        name : string
            Identifier for this station.
        x : float
            x-coordinate for this station.
        y : float
            y-coordinate for this station.
        """
        self.name = str(name)
        self.passengers = np.array([])
        self.xy = np.array([np.float64(x),np.float64(y)])

    def spawn(self):
        """Generic stations don't spawn anything"""
        return np.array([])

    def kill(self):
        """Not killing anything"""
        return np.array([])

    def update(self,destinations=set(),instructions=dict()):
        for p in self.passengers:
            p.update()

        #Spawn new passengers.
        self.passengers = np.union1d(self.passengers, np.array(self.spawn(set(destinations) ^ set([self]), instructions)))
        #TODO: This is optional, will only happen on KillerStation.
        self.passengers = np.setdiff1d(self.passengers,self.kill(), assume_unique=True)


class BasicStation(Station):
    """
    Create a simple station.

    Parameters
    ----------
    name : string
        Identifier for this station.
    x : float
        x-coordinate for this station.
    y : float
        y-coordinate for this station.
    minpas : int
        Minimum number of passengers to spawn per timestep
    maxpas : int
        Maximum number of passengers to spawn per timestep


    Attributes
    ----------
    name : string
        identifier for this station
    passengers : numpy.array
        array of Passenger objects that are at current station
    xy : numpy.array([float,float])
        pair of x,y coordinates to specify stations location


    """
    def __init__(self, name,x,y, minpas,maxpas):
        "Use parent __init__ function"
        super(BasicStation,self).__init__(name, x, y)
        self.minpas = minpas
        self.maxpas = maxpas
        return

    def spawn(self,destinations,instructions):
        """Spawn passengers
        """
        num = random.randint(self.minpas,self.maxpas)
        newpassengers = np.array([])
        for _ in itertools.repeat(None,num):
            newpassengers = np.append(newpassengers, Passenger(self,random.sample(destinations, 1)[0], instructions))
        return newpassengers

    def __repr__(self):
        """
        Representation of Station as a string
        """
        return "St'%s'"%self.name

class KillerStation(BasicStation):
    """Kills random people
       For testing purposes until passengers are able to move
       Code runs much faster if there are less passengers
    """

    def kill(self):
        """kill random passengers"""
        killcount=random.randint(0,len(self.passengers))
        kills= set(random.sample(self.passengers,killcount))
        return kills

class LineStation(BasicStation):
    """
    Create station that knows which lines go through it
    """
    def __init__(self, name,x,y, minpas,maxpas,lines):
        "Use parent __init__ function"
        super(LineStation,self).__init__(name, x, y,minpas,maxpas)
        #Lines is a set of strings.
        #These strings NEED! to match the identifier for the Line objects.
        self.lines = set(lines)
        return

#    def update(self,destinations=set(),instructions=dict()):
#        super(LineStation,self).update(destinations,instructions)
#        for p in self.passengers:
#            for t in p.transfers:
#                for l in t[1]:
#                    if l not in self.lines:
#                        print repr(self), p.transfers

    def __repr__(self):
        """
        Representation of Station as a string
        """
        return "St'%s:%s'"%(self.name,self.lines)



class Passenger(object):
    """Wants to go from A to B"""
    def __init__(self, origin, destination,instructions, verbose=0):
        self.origin = origin
        self.location = origin
        self.destination = destination
        self.transfers = np.array(instructions[self.origin,self.destination])
        self.verbose = verbose
        return

    def update(self,location=None):
        if location:
            self.location = location

    def __repr__(self):
        s = "Passenger\n"
        s += "From:%s\n"%self.origin.name
        s += "To:%s\n"%self.destination.name
        s += "At:%s\n"%self.location
        s += "By%s\n"%self.transfers
        return s

    def __del__(self):

        if self.verbose >0:
            print "Deleted at %s."%self.location.name

        return


class Train(object):
    """Moves passengers from station to station."""
    def __init__(self, name, capacity, line, start, direction, velocity, verbose=0):
        """ARGUMENTS
        name - Identifier for this train, e.g. "F-1".
        capacity - Max number of people on one train.
        line - Line object, in charge of destinations
        start - initial station
        direction - forward (1) or reverse (-1)
        velocity - meters per time step
        verbose - degree of verbosity (int, 0 = quiet, 1= info, 2 = debug)
        """
        self.name = str(name)
        self.capacity = int(capacity)
        self.line = line
        self.current_station = start
        self.direction=direction
        if not direction in [1, -1]:
            raise Exception, "Direction is either forward (1) or reverse (-1)."
        self.v = np.float64(velocity)
        self.verbose = verbose
        self.passengers = np.array([])
        #Determine the next station.
        self.next_station, self.direction =line.resolve(self.current_station, self.direction)
        #Calculate distance between current and next station.
        self.d2s = self.distance_to_stop(self.current_station,self.next_station)
        #Distance traveled since last station.
        self.traveled = np.float64()
        if self.verbose >1: print "Train %s: New train at location '%s'."%(self.name, self.current_station.name)
        return

    def distance_to_stop(self,origin,destination):
        """Get the distance to the next stop"""
        #TODO see if table lookup is faster than calculation
        dist = np.linalg.norm(destination.xy - origin.xy)
        return dist

    def update(self):
        """Iterate 1 timestep"""
        at_station = False
        self.traveled += self.v #TODO make velocity independent of timestep?
        if self.verbose > 2:
            print "Train %s: Traveled %.3f meters."%(self.name, self.v)
            print "Train %s: Is carrying %d passenger(s)"%(self.name, len(self.passengers))
        if self.traveled >= self.d2s:
            at_station = True

        if at_station:
            self.current_station = self.next_station
            self.next_station, self.direction = self.line.resolve(self.current_station, self.direction)
            self.load_unload()
            self.d2s = self.distance_to_stop(self.current_station,self.next_station)
            self.traveled = np.float64()

            if self.verbose > 1: print "Train %s: Reached destination '%s'"%(self.name, self.current_station.name)
            if self.verbose > 1: print "Train %s: Next destination is '%s'"%(self.name, self.next_station.name)
            if self.verbose > 1: print "Train %s: Direction is '%d'"%(self.name, self.direction)
        return

    def load_unload(self):
        """Exchange passengers with station"""

        #Passengers that are getting off.
        offload = np.array([])
        transfer = np.array([])

        #Counters for diagnostics
        off_count = int()
        on_count = int()
        transfer_count = int()

        #First, passengers need to get off to free up space on the train.
        for pas in self.passengers:
            pas.update(location=self.current_station)
            #Offload and disappear if this is their final destination.
            try:
                if pas.destination == pas.location:
                    offload = np.append(offload,pas)
                    off_count +=1
                #If a passenger needs a transfer here, add them to the transfer list.
                elif pas.location == pas.transfers[0][0]:
                    transfer = np.append(transfer,pas)
                    transfer_count +=1
            except IndexError:
                pass

        #Passengers are removed from the train.
        self.passengers = np.setdiff1d(self.passengers,  np.union1d(offload, transfer))
        self.current_station.passengers = np.union1d(self.current_station.passengers, transfer)

        #Now, see which passengers are getting on
        for pas in self.current_station.passengers:

            #Dont take passengers if the train is full
            if len(self.passengers) >= self.capacity:
                break

            #If a passenger has no transfers, skip him
            if not len(pas.transfers):
                continue

            #Get passengers details
            pstation,pline,pdirection = pas.transfers[0]

            ##If this is not the right station, line or direction, dont get on
            if pstation != self.current_station or self.line.name not in pline:
                
                continue

            #check what direction the passenger needs to go
            pline_index= pline.index(self.line.name)
            if pdirection[pline_index] != self.direction:
                #if the direction dont match, dont get on.
                continue


            #Everything checks out. Begin the boarding process.
            index=np.where(self.current_station.passengers==pas)
            self.current_station.passengers = np.delete(self.current_station.passengers,index)
            self.passengers = np.append(self.passengers,pas)
            #Take this transfer out of passenger list of transfers
            pas.transfers = pas.transfers[1:]
            #Please mind the closing doors.
            on_count += 1

        if self.verbose >1:
            print "Train %s: Passengers getting off at station '%s': %d"%(self.name, self.current_station.name, off_count)
            print "Train %s: Passengers making transfer at station '%s': %d"%(self.name, self.current_station.name, transfer_count)
            print "Train %s: Passengers getting on at station '%s': %d"%(self.name, self.current_station.name, on_count)
        elif self.verbose >0:
            print "Train %s: At station '%s' On/Off/Transfer: %d/%d/%d"%(self.name, self.current_station.name, on_count, off_count, transfer_count)

        return


class Line(object):
    """
    Set of instructions that provide a train with it's route

    Parameters
    ----------
    name : string,
        The name to represent this line.
    route : array_like,
        Sequence that details which stations follow in which order.
    """

    def __init__(self, name, route):
        self.name = str(name)
        self.route = np.array(route)
        for x in self.route:
            if not issubclass(type(x), Station):
                raise Exception, "Invalid line, one of your entries is not a Station."
        return

    def resolve(self, station, direction):
        """Based on the direction that you are traveling, return next or previous."""
        if not direction in [1,-1]:
            raise Exception, "Direction is forward (1), or reverse (-1)."

        #Find index of current station, to lookup where the next station is.
        index = np.where(self.route==station)[0][0]
        indir = index + direction
        
        #If we are approaching last stop on reverse, indir == -1
        if indir < 0:
            #Flip the train forward, and set next station to station 1
            direction *=-1
            indir = 1            
        #Catching IndexError to flip direction if at end on forward.
        try:
            self.route[indir]
        except IndexError:
            direction *= -1
            indir = index + direction
            
        return ([self.route[indir], direction])

class CircleLine(Line):
    """
    Subclass of Line. Handles circle lines
    """
    def resolve(self, station, direction):
        """Based on the direction that you are traveling, return next or previous."""
        if not direction in [1,-1]:
            raise Exception, "Direction is forward (1), or reverse (-1)."

        #Find index of current station, to lookup where the next station is.
        index = np.where(self.route==station)[0][0]
        indir = index + direction
        #Catching IndexError to go back to first station on line
        try:
            self.route[indir]
        except IndexError:
            indir = 0

        return ([self.route[indir], direction])


#FUNCTIONS####################################################################


def pairwise(sequence):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    pairs=list()
    for i in range(len(sequence)-1):
        pairs.append([sequence[i],sequence[i+1]])

    return pairs


def shortest_transfer(a,b, linegraph,offset=1):
    """
    Calculate shortest transfer path(s) for each pair of lines between stations.
    
    Arguments
    ---------
    a - LineStation,
        LineStation object origin
    b - Linestation,
        Linestation object destination
    linegraph - networkx.Graph()
        networkx graph object with connectivity of the lines
    offset - int [default = 1]
        will return solutions  <= shortest+offset
    """
    alines = a.lines
    blines = b.lines
    
    somesolutions = list()
    least_transfers= list()
    for a in alines:
        for b in blines:
            solutions = nx.all_shortest_paths(linegraph,a,b)
            for solution in solutions:
                somesolutions.append(solution)
    short = 25
    for solution in somesolutions:
        if len(solution) < short:
            short = len(solution)
    for solution in somesolutions:
        if len(solution) <= short +offset:
            least_transfers.append(solution)
    return least_transfers

def reduce_to_uniques(least_transfers):
    uniquelines = list()
    for b in least_transfers:
        for l in b:
            if l not in uniquelines:
                uniquelines.append(l)
    return uniquelines

    

###### OLD SLOW ALGORITMS, BEWARE ######










def travel_instructions(subway=nx.Graph(),lines=dict(),order=["transfers","stops","distance"],cutoff=70):
    """
    Provide a dictionary of travel instructions based on the paths, distances, transfers and amount of stops.

    Arguments
    ---------
    subway - networkx.Graph(),
        Graph with connectivity of all the stations.
    lines - dict(),
        Dictionary containing all the lines.
    order - list() [default: ["transfers","stops","distance"]]
        List of length 3, prioritize transfers, stops or distance on optimal route.
    """
    pathmatrix = generate_allpaths(subway,cutoff)
    distmatrix = generate_dist_line(pathmatrix)
    transmatrix = generate_transfers(distmatrix,lines)
    bestmatrix = decide_on_path(transmatrix,order)
    simplematrix = simplify_matrix(bestmatrix)
    return simplematrix





def generate_allpaths(graph,cutoff):
    """
    Generate all routes for a passenger to take through the subway that only pass a station once
    """
    pathmatrix = dict()
    for outer in graph.nodes_iter():
        for inner in graph.nodes_iter():
                pathmatrix[tuple([outer,inner])] = list(nx.all_simple_paths(graph,outer,inner,cutoff=cutoff))
    return pathmatrix

def generate_dist_line(pathmatrix):
    """
    calculate the distances belonging to a set of paths and the line along the route

    Returns
    -------
    distmatrix : dict,
    distmatrix contains station pairs as keys, points to possible paths, with lines taken along paths, and total distance of the path
    Example:
    distmatrix[a,d]  :  ([[a,b,c,d],...], ['1','1','1'], 82.09)
    """
    distmatrix = dict()
    for key,paths in pathmatrix.iteritems():
        dists=list()
        lines=list()
        for path in paths:
            dist = np.float64()
            line = list()
            for stationa,stationb in pairwise(path):
                dist += np.linalg.norm([stationa.xy,stationb.xy])
                line.append(stationa.lines & stationb.lines)
            dists.append(dist)
            lines.append(line)
        distmatrix[key]=zip(paths,lines,dists)
    #
    return distmatrix

x = list()


def generate_transfers(distmatrix,lines):
    """
    Generate optimal choice of line to take per path
    Calculate amount of transfers for that line
    """
    transmatrix = dict()
    #Per station pairs i,j.
    for key,paths in distmatrix.iteritems():
        #A given path between station i,j
        bestpaths=list()
        for path in paths:
            stations=path[0]
            #figure out the best path one could take
            bestpath = sets_to_lists(consistent_resolver(path[1]))
            directions = list()
            #every station pairs, figure out direction you're traveling
            for connections,pair in enumerate(pairwise(stations)):

                direction = list()
                #check it for every line in the list of options
                for con in bestpath[connections]:
                    ordera = np.where(lines[con].route==pair[1])
                    orderb = np.where(lines[con].route==pair[0])
                    if ordera > orderb:
                        direction.append(1)
                    elif ordera < orderb:
                        direction.append(-1)
                    else:
                        raise Exception, "Something weird with the directions."
                directions.append(direction)

            ntransf = count_transfers(bestpath,directions)
            dist = path[2]
            #station is combined with lines that one could take there
            #the last station is removed from the list since no train is taken
            #between every station we will have
            #  list of paths
            #      #every path
            #        list
            #          list of stations in path
            #          list of lines optimal for that path
            #          list of directions of line for that path
            #        list
            #          total transfers
            #          total stops
            #          total distance
            bestpaths.append((tuple(zip(stations,bestpath,directions)), tuple([ntransf,len(bestpath),dist])))
        transmatrix[key] = bestpaths
    return transmatrix

def decide_on_path(transmatrix,order=["transfers","stops","distance"]):
    """
    Choose the best path depending on criterium.
    """
    bestmatrix = dict()

    if not len(order) ==3:
        raise Exception, "Invalid length order %d. Must be 3,"%len(order)
    norder = [None,None,None]
    for i,x in enumerate(order):
        if x == "transfers":
            norder[i] = 0
        elif x == "stops":
            norder[i] = 1
        elif x == "distance":
            norder[i] = 2
        else:
            raise Exception,"Invalid element in order: %s.\nMust be transfers,stops,or distance."%x


    #Per station pairs i,j.
    for key,paths in transmatrix.iteritems():
        #A given path between station i,j
        bestmatrix[key]=sort_paired_triplet_by(paths,norder,1)[0]
    return bestmatrix

def simplify_matrix(bestmatrix):
    """
    Generate a list of tranfer stations for passengers to use.
    """
    simplematrix = dict()
    for key,path in bestmatrix.iteritems():
        simplematrix[key] = simplify_path(path)
    return simplematrix


def simplify_path(path):
    """
    Reduce path to transfers
    """
    reduced = list()

    reduced.append(path[0][0])
    for station in path[0]:
        #if the last station in the path is not on the same line and direction
        if not reduced[-1][1] == station[1] or not reduced[-1][2] == station[2]:
            #This station is a transfer
            reduced.append(station)
    return reduced

def sort_paired_triplet_by(unsortedlist,order,where):
    """
    Sort a list of triplets that is paired with something else

    Arguments
    ---------
    unsortedlist - list of two dimensions, with one element of length 3
    order - list of length 3
        order by which to sort [0,1,2] sorts by element 0, then 1, then 2.
    where - int 0,1
        Is the triplet the first, or second element in the pairs.

    Examples
    -------
    >>>myunsortedlist=[[["abc"],[1,2,3]],[["bcd"],[1,3,4]],[["bac"],[2,1,4]],[["xxa"],[5,5,1]]]

    >>>print tools.sort_paired_triplet_by(myunsortedlist,[2,1,0],1)

    [[['xxa'], [5, 5, 1]], [['abc'], [1, 2, 3]], [['bac'], [2, 1, 4]], [['bcd'], [1, 3, 4]]]
    """
    x1,x2,x3=order
    sortedlist= sorted(unsortedlist,key=lambda x: [x[where][x1],x[where][x2],x[where][x3]] )
    return sortedlist

def sort_triplet_by(unsortedlist,order):
    """
    Sort a list of triplets
    """
    x1,x2,x3=order
    sortedlist= sorted(unsortedlist,key=lambda x: [x[x1],x[x2],x[x3]] )
    return sortedlist

def sets_to_lists(los):
    """
    list of sets to list of lists
    """
    lol = list()
    for s in los:
        lol.append(list(s))
    return lol

def consistent_resolver(opt_per_stat,capture=True):
    """
    Arguments
    ---------
    opt_per_stat - list of sets
        Set with possible lines that connect stations

    Makes sure that the path resolved is consistent in both directions
    This reduces transfers in total, since it also checks from back to
    front for better options.
    """
    forward = list(opt_per_stat)
    reverse = list(forward[::-1])

    ans_for = transfer_resolver(forward)
    ans_rev = transfer_resolver(reverse)
    rev_ans_for = transfer_resolver(ans_for[::-1])
    rev_ans_rev = transfer_resolver(ans_rev[::-1])

    if ans_for == ans_rev[::-1]:
        # "results are same in reverse"
        if ans_for == rev_ans_for[::-1]:
            #"results are consistent"
            return ans_for
        elif rev_ans_for[::-1] == rev_ans_rev:
            # "consistent after reversing twice"
            return rev_ans_rev
        else:
            # "Cant make consistent, assume equally good solutions exist"
            if capture: weirdpaths.append(rev_ans_rev)
            return rev_ans_rev

    else:
        # "not the same in reverse"
        if rev_ans_for[::-1] == ans_for:
            # "results are consistent"
            return rev_ans_for[::-1]
        elif rev_ans_for[::-1] == rev_ans_rev:
            # "consistent after reversing twice"
            return rev_ans_rev
        else:
           # "Cant make consistent, assume equally good solutions exist"
            if capture: weirdpaths.append(rev_ans_rev)
            return rev_ans_rev

def transfer_resolver(opt_per_stat):
    """
    Find optimal list of transfers in one direction
    """
    opt_per_stat = list(opt_per_stat)
    opt_copy = list(opt_per_stat)
    #for every element in the list of lines
    for i in range(len(opt_per_stat)):
        try:
            insect = opt_copy[i] & opt_copy[i+1]
            if insect:
                opt_copy[i]= insect
            else:
                pass
        except IndexError:
            othersect = opt_copy[i] & opt_copy[i-1]
            if othersect:
                opt_copy[i] = othersect
            break

    if opt_copy == opt_per_stat:
        return opt_copy
    else:
        return transfer_resolver(opt_copy)

def count_transfers(linlist,directions):
    """
    Arguments
    ---------
    linlist - list of lists
        list with list of lines to follow in order
    directions - list of lists
        direction along the particular line
    Returns
    -------
    transfers - int
        The number of transfers in this set
    """
    transfers = int()
    try:
        for i,ld in enumerate(zip(linlist,directions)):
            #if a passenger changes lines, that is a transfer
            if linlist[i]  != linlist[i+1]:
                transfers += 1
            #if a passenger changes direction on the same line
            #he also needs to transfer. Odd situation though.
            elif directions[i] != directions[i+1]:
                transfers +=1
            else:
                continue

    except IndexError:
        pass
    return transfers

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

def nyc_map(graph,file_name=None):
    """Visually represent the subway network and save to file"""
    # Turn interactive plotting off
    plt.ioff()
    positions = dict()
    labels = dict()
    for node in graph.nodes_iter():
        positions[node] = node.xy
        labels[node] = ""
    plt.figure()
    nx.draw_networkx(graph,positions,labels=labels,node_size=50,node_color='chartreuse')
    if file_name:
        plt.savefig(file_name, dpi=300)
    else: plt.show()
