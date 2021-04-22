import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
from math import *  # just to get some math functions(sqrt)
import math


class rtmaps_python(BaseComponent):
    # constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

        self.R = 6371009  # this is the radius of the earth in meters

    # configuration des I/O
    def Dynamic(self):

        self.add_input("x_y", rtmaps.types.ANY)  # coordonnees dans le repere local du robot
        self.add_output("distancePoint", rtmaps.types.AUTO)
        self.add_output("angle_erreur", rtmaps.types.AUTO);  # the angle between the two points in rad

    # appel a la creation
    def Birth(self):
        print("starting...");

    # called every input
    def Core(self):

        # calculating the distance between the robot and the point
        #0 et 1
        X=self.inputs["x_y"].ioelt.data[0]
        Y=self.inputs["x_y"].ioelt.data[1]
        
        #Calcul de la distance au point suivant
        distancePoint = sqrt((X ** 2) + (Y ** 2))
        
        
        
        #k = (self.inputs["Eb"] + self.inputs["Ea"]) / 2
        #D = sqrt(((0.9996 * d) ** 2)) * ((k + self.R) / self.R)

        # Calculating the angle between the point of the robot and the point(in rad)
        #k = (self.inputs["UTMya"] - self.inputs["UTMyb"]) / (self.inputs["UTMxa"] - self.inputs["UTMxb"])
        
        
        angle = math.atan2(X,Y)  # the angle in rad

        # Sending D as an output
        self.outputs["distancePoint"].write(distancePoint)

        # Sending 'angle' as an output
        self.outputs["angle_erreur"].write(angle)

    # destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass