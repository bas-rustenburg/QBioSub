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

    def update(self,destinations=set()):
        #Spawn new passengers.
        self.passengers = np.union1d(self.passengers, np.array(self.spawn(set(destinations) ^ set([self]) )))
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

    def spawn(self,destinations):
        """Spawn passengers
           TODO remove current station from the list?"""
        num = random.randint(self.minpas,self.maxpas)
        newpassengers = np.array([])
        for _ in itertools.repeat(None,num):
            newpassengers = np.append(newpassengers, Passenger(self,random.sample(destinations, 1)[0]))
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


class Passenger(object):
    """Wants to go from A to B"""
    total=0
    def __init__(self, origin, destination, verbose=False):
        self.origin = origin
        self.location = origin
        self.destination = destination
        self.transfer = np.array([])
        self.verbose = verbose
        Passenger.total +=1
        return

    def route(self):
        """Solve the route that the passenger will take"""
        self.route=np.array([])
        self.line=str()
        return

    def __del__(self):
        Passenger.total -= 1
        if self.verbose:
            print "Please don't kill me, I have a family!"
            print "I'm being killed at %s."%self.location.name

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
        self.next_station, self.direction =line.resolve(self.direction, self.current_station)
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
            self.next_station, self.direction = self.line.resolve(self.direction, self.current_station)
            self.load_unload(self.current_station)
            self.d2s = self.distance_to_stop(self.current_station,self.next_station)
            self.traveled = np.float64()

            if self.verbose > 1: print "Train %s: Reached destination '%s'"%(self.name, self.current_station.name)
            if self.verbose > 1: print "Train %s: Next destination is '%s'"%(self.name, self.next_station.name)
        return

    def load_unload(self, station):
        """Exchange passengers with station"""

        #Passengers that are getting off.
        offload = np.array([])
        transfer = np.array([])
        off_count = int()
        on_count = int()
        transfer_count = int()

        #First, passengers need to get off to free up space on the train.
        for pas in self.passengers:

            #Offload and disappear if this is their final destination.
            if pas.destination == station:
                offload = np.append(offload,pas)
                off_count +=1
            #If a passenger needs a transfer here, add them to the transfer list.
            elif station in pas.transfer:
                transfer = np.append(transfer,pas)
                transfer_count +=1

        #Passengers are removed from the train.
        self.passengers = np.setdiff1d(self.passengers,  np.union1d(offload, transfer))

        #TODO: Once passengers can choose the right train, add stations transfer passengers here

        #Now, see which passengers are getting on
        #TODO: Passengers need to figure out if they want to get on this train.
        try:

            #Keep running forever
            while True:
                #We stop of the train is full
                if len(self.passengers) >= self.capacity:
                    break
                #This will return IndexError once the station is empty
                #TODO Dictionary lookup with trains Line to get list of passengers that ACTUALLY need to board
                pas = station.passengers[0]
                index=np.where(station.passengers==pas)

                station.passengers = np.delete(station.passengers,index)
                np.append(self.passengers,pas)
                on_count += 1
        except IndexError:
            #IndexError would mean there are no passengers left in the station, so we're done.
            pass

        finally:
            #TODO: Once passengers will only get on the right train , move this up
            station.passengers = np.union1d(station.passengers, transfer)

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

    def resolve(self,direction, station):
        """Based on the direction that you are traveling, return next or previous."""
        if not direction in [1,-1]:
            raise Exception, "Direction is forward (1), or reverse (-1)."

        #Find index of current station, to lookup where the next station is.
        index = np.where(self.route==station)[0][0]
        indir = index + direction
        #Catching IndexError to flip direction if at end.
        try:
            self.route[indir]
        except IndexError:
            direction *= -1
            indir = index + direction
        finally:
            #If we're at the beginning, flip
            if indir == 0:
                direction *= -1
            return ([self.route[indir], direction])




def pairwise(sequence):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    pairs=list()
    for i in range(len(sequence)-1):
        pairs.append([sequence[i],sequence[i+1]])

    return pairs

def generate_routes(graph):
    """
    Generate all routes for a passenger to take through the subway that only pass a station once
    """
    pathmatrix = dict()
    for outer in graph.nodes_iter():
        for inner in graph.nodes_iter():
                pathmatrix[tuple([outer,inner])] = list(nx.all_simple_paths(graph,outer,inner))
    return pathmatrix

def generate_dist_line(pathmatrix):
    """
    calculate the distances belonging to a set of paths and the line along the route
    
    Returns
    -------
    dmatrix : dict,
    Dmatrix contains station pairs as keys, points to possible paths, with lines taken along paths, and total distance of the path
    Example:
    dmatrix[a,d]  :  ([[a,b,c,d],...], ['1','1','1'], 82.09)
    """
    dmatrix = dict()
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
        dmatrix[key]=zip(paths,lines,dists)
    #
    return dmatrix

x = list()


def generate_transfers(dmatrix,lines):
    """
    Generate optimal choice of line to take
    """
    tmatrix = dict()
    #Per station pairs i,j.
    for key,paths in dmatrix.iteritems():
        #A given path between station i,j
        newpaths=list()
        for path in paths:
            stations=path[0]
            #figure out the best path one could take            
            bestpath = sets_to_lists(consistent_resolver(path[1]))
            print len(stations),len(bestpath)
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
            print len(stations),len(bestpath)
            newpaths.append((zip(stations,bestpath,directions),dist,ntransf))
        tmatrix[key] = newpaths
    return tmatrix



#Some lists to throw at the consistent_resolver
xlist = [{1,2}, {1,2}, {2}, {2}, {3}]
vlist = xlist[::-1]
ylist = [{1,4,3},{2,4,3},{1,2,3},{2},{3},{3,2}]
zlist = ylist[::-1]
alist = [{1,2,5}, {1,2}, {1,2,4} ]
blist = alist[::-1]

def sets_to_lists(los):
    """
    list of sets to list of lists
    """
    lol = list()
    for s in los:
        lol.append(list(s))
    return lol

def consistent_resolver(opt_per_stat):
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
#        print "solution found %s" % opt_copy        
        return opt_copy
    else:
#        print "no solution yet"
#        print "%s x\n%s"%(opt_copy, opt_per_stat)
        return transfer_resolver(opt_copy)

def count_transfers(linlist,directions):
    """
    Arguments
    ---------
    linlist - list of sets
        list with set of lines to follow in order
    
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


