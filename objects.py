# -*- coding: utf-8 -*-
"""
Created on Tue May 13 18:13:26 2014

@author: B-Rus, Hy-C
"""

import random
import itertools
import numpy as np

class Station(object):
    """Spawns passengers, eats passengers
    """
    def __init__(self,name,x,y):
        self.name = name 
        self.passengers = set()
        self.trains = set()
        self.xy = np.array([np.float64(x),np.float64(y)])
        
    def spawn(self):
        """Generic stations don't spawn anything"""
        return set()
    def kill(self):
        """Not killing anything"""
        return set()
        
    def update(self,destinations=set()):
        #spawn the new.
        self.passengers = self.passengers | self.spawn(destinations)
        #Kill passengers that have reached destination.
        #TODO make this a function that happens in trains by offloading them to nowhere.
        self.passengers = self.passengers - self.kill()
        

class BasicStation(Station):
    """Simple station
       Kills passengers if they have reached their destination
    """
    def __init__(self, name,x,y, minpas,maxpas):
        "Use parent __init__ function"
        super(BasicStation,self).__init__(name, x, y)
        
        self.minpas = minpas
        self.maxpas = maxpas        
        
    def spawn(self,destinations):
        """Spawn passengers
           TODO remove current station from the list?"""        
        num = random.randint(self.minpas,self.maxpas)
        newpassengers = set()    
        for _ in itertools.repeat(None,num):
            newpassengers.add(Passenger(self,random.sample(destinations, 1)))
        return newpassengers
        
    def kill(self):
        """kill those that have reached their destination."""
        kills=set()
        for pas in self.passengers:
            if pas.location == pas.destination:
                kills.add(pas)
        return kills
        
class KillerStation(BasicStation):
    """Simple station
       Kills random people
       For testing purposes until passengers move
       Code much faster if there are less passengers
    """
       
    def kill(self):
        """kill random passengers"""
        killcount=random.randint(0,len(self.passengers))
        kills= set(random.sample(self.passengers,killcount))
        return kills

        zip()
      

class Passenger(object):
    """Wants to go from A to B"""
    total=0
    def __init__(self, origin, destination, verbose=False):
        self.origin = origin
        self.location = origin
        self.destination = destination
        self.transfer = set()
        self.line = str()
        self.verbose = verbose
        Passenger.total +=1
#   
    def route(self):
        """Solve the route that the passenger will take"""
        self.route=list()
        self.line=str()
        pass        
    
    def __del__(self):
        if self.verbose:
            print "Please don't kill me, I have a family!"
            print "I'm being killed at %s."%self.location.name
        Passenger.total -= 1
        
        
class Train(object):
    """Moves passengers from station to station."""
    def __init__(self, line,origin, destination,velocity=np.float64(1.0), capacity=150,at_station=False, verbose=False):
        """ARGUMENTS
        line - line name/number
        origin - previous station
        destination - next station        
        """
        self.line = str(line)        
        self.v = np.float64(velocity)
        self.passengers = set()
        self.origin = origin
        self.destination=destination
        self.capacity = capacity
        self.d2s = self.distance_to_stop(self.origin,self.destination)
        self.traveled = np.float64()
        self.at_station = at_station
        self.verbose = verbose
        
    def distance_to_stop(self,origin,destination):
        """Get the distance to the next stop
        TODO see if table lookup is faster than calculation"""
        print destination
        dist = np.linalg.norm(destination.xy - origin.xy)
        return dist
        
    def update(self):
        """Iterate 1 timestep"""
        self.traveled += self.v
        if self.traveled >= self.d2s:
            if self.verbose: print "Reached destination %s"%self.destination.name
            self.at_station = True
        
        if self.at_station:
            self.load_unload(self.destination)
       
    def next_station(self,current_station, line,direction=1):
        """Resolve what the next station will be upon arrival."""
        next_station = line.resolve(direction, self.current_station)
        return next_station
            
    def load_unload(self, station):
        """Exchange passengers with station"""
        #Passengers get off
        offload = set()
        transfer = set()
        for pas in self.passengers        :
            if pas.destination == station:
                offload.add(pas)
            elif station in pas.transfer:
                transfer.add(pas)        
        self.passengers -= offload + transfer
        #passengers that are at their destination will be garbage collected.
        for pas in station.passengers:
            if pas.line == self.line:
                try:
                    while not len(self.passengers) == self.capacity:
                        self.passengers.add(station.passengers.pop())    
                except KeyError:
                    pass
                
        station.passengers.add(transfer)
        return
        
    
class Line(object):
    """TODO
    Currently a dummy
    Should be a set of instructions that manipulates a trains d2s"""
    def __init__(self):
        self.route = list()
        for x in self.route:
            if not type(x) == Station:
                raise Exception, "Invalid line"
                
    def resolve(self,direction, station):
        """Based on the direction that you are traveling, return next or previous."""
        if not direction in [1,-1]:
            raise Exception, "Direction is forward (1), or reverse (-1)."
            
        index = self.route.index(station)
        return self.route[direction + index ]
        
        
##maps = nx.Graph(city="New NYC")
##
##maps.add_node("sta")