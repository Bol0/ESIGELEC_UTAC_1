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

    # configuration des I/O
    def Dynamic(self):
        self.add_input("UTMx", rtmaps.types.ANY)
        self.add_input("UTMy", rtmaps.types.ANY)
        self.add_input("euler", rtmaps.types.ANY)
        
        self.add_output("D", rtmaps.types.AUTO);  # distance between those 2 points through an uneven terrain
        self.add_output("angle", rtmaps.types.AUTO);  # the angle between the two points in rad

    # appel a la creation
    def Birth(self):
        print("starting...");

    # called every input
    def Core(self):

        # calculating the distance between the robot and the point
        d = sqrt(
            ((self.inputs["UTMxa"] - self.inputs["UTMxb"]) ** 2) + ((self.inputs["UTMya"] - self.inputs["UTMyb"]) ** 2))
        k = (self.inputs["Eb"] + self.inputs["Ea"]) / 2
        D = sqrt(((0.9996 * d) ** 2)) * ((k + self.R) / self.R)

        # Calculating the angle between the point of the robot and the point(in rad)
        k = (self.inputs["UTMya"] - self.inputs["UTMyb"]) / (self.inputs["UTMxa"] - self.inputs["UTMxb"])
        angle = 1.578 - math.atan(k)  # the angle in rad

        # Sending D as an output
        self.outputs["D"].write(D)

        # Sending 'angle' as an output
        self.outputs["angle"].write(angle)

    # destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass
