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
        #self.add_input("UTMxa", rtmaps.types.ANY)  # current x position of the robot
        #self.add_input("UTMya", rtmaps.types.ANY)  # current y position of the robot
        #self.add_input("UTMxb", rtmaps.types.ANY)  # x position of the ping
        #self.add_input("UTMyb", rtmaps.types.ANY)  # y position of the ping
        #self.add_input("Eb", rtmaps.types.ANY)  # elevation of point B
        #self.add_input("Ea", rtmaps.types.ANY)  # elevation of point A
        self.add_input("x_y", rtmaps.types.ANY)  # elevation of point B
        self.add_output("angle_distance", rtmaps.types.AUTO);  # the angle between the two points in rad

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
