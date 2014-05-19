# -*- coding: utf-8 -*-
"""
Created on Tue May 13 18:13:26 2014

@author: Bas Rustenburg, Hyunwoo Cho
"""

import random
import itertools
import numpy as np

class Station(object):
    """Station object
    """
    def __init__(self,name,x,y):
        self.name = name
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
        newpassengers = np.array([])
        for _ in itertools.repeat(None,num):
            newpassengers = np.append(newpassengers, Passenger(self,random.sample(destinations, 1)[0]))
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