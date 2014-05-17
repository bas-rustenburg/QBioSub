# -*- coding: utf-8 -*-
"""
Created on Tue May 13 18:13:26 2014

@author: B-Rus, Hy-C
"""

import random
import itertools
import numpy as np

class Station(object):
    """Station object
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
        #Spawn new passengers.
        self.passengers = self.passengers | self.spawn(set(destinations) ^ set([self]) )
        #TODO: This is optional, will only happen on KillerStation.
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
        return

    def spawn(self,destinations):
        """Spawn passengers
           TODO remove current station from the list?"""
        num = random.randint(self.minpas,self.maxpas)
        newpassengers = set()
        for _ in itertools.repeat(None,num):
            newpassengers.add(Passenger(self,random.sample(destinations, 1)[0]))
        return newpassengers


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


class Passenger(object):
    """Wants to go from A to B"""
    total=0
    def __init__(self, origin, destination, verbose=False):
        self.origin = origin
        self.location = origin
        self.destination = destination
        self.transfer = set()        
        self.verbose = verbose
        Passenger.total +=1
        return

    def route(self):
        """Solve the route that the passenger will take"""
        self.route=list()
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
        self.passengers = set()

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
            if self.verbose > 0: print "Train %s: Reached destination '%s'"%(self.name, self.current_station.name)
            self.next_station, self.direction = self.line.resolve(self.direction, self.current_station)
            if self.verbose > 1: print "Train %s: Next destination is '%s'"%(self.name, self.next_station.name)
            self.load_unload(self.current_station)
            self.d2s = self.distance_to_stop(self.current_station,self.next_station)
            self.traveled = np.float64()
            
        return   

    def load_unload(self, station):
        """Exchange passengers with station"""
        
        #Passengers that are getting off.
        offload = set()
        transfer = set()
        off_count = int()
        on_count = int()
        transfer_count = int()
        for pas in self.passengers:
            if pas.destination == station:
                offload.add(pas)
                off_count +=1
            elif station in pas.transfer:
                transfer.add(pas)
                transfer_count +=1
        self.passengers -= offload | transfer
                        
        try:
            while True:
                if len(self.passengers) == self.capacity:
                    break
                self.passengers.add(station.passengers.pop())
                on_count += 1
        except KeyError:
            pass

        if self.verbose >1:
            print "Train %s: Passengers getting off at station '%s': %d"%(self.name, self.current_station, off_count)
            print "Train %s: Passengers making transfer at station '%s': %d"%(self.name, self.current_station, transfer_count)        
            print "Train %s: Passengers getting on at station '%s': %d"%(self.name, self.current_station, on_count) 
        station.passengers |= transfer
     
        #passengers that are at their destination will be garbage collected.
        return


class Line(object):
    """Set of instructions that provide a train with it's route"""
    def __init__(self, name, route):
        self.name = str(name)
        self.route = route
        for x in self.route:
            if not issubclass(type(x), Station):
                raise Exception, "Invalid line"

    def resolve(self,direction, station):
        """Based on the direction that you are traveling, return next or previous."""
        if not direction in [1,-1]:
            raise Exception, "Direction is forward (1), or reverse (-1)."
        index = self.route.index(station)
        try:
            self.route[direction + index ]
        except IndexError:
            direction *= -1
        finally:
            return ([self.route[direction + index], direction])