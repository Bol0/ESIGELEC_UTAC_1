import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
from math import *  # just to get some math functions(sqrt)
import math

liste_points = [[0,0]]

class rtmaps_python(BaseComponent):
    # constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    # configuration des I/O
    def Dynamic(self):
        self.add_input("UTM_vehicule_euler", rtmaps.types.ANY)
        self.add_input("UTM_trajectoire", rtmaps.types.ANY)
        self.add_output("x_y", rtmaps.types.AUTO);  # distance between those 2 points through an uneven terrain

    # appel a la creation
    def Birth(self):
        print("starting...");

    # called every input
    def Core(self):
        print(self.input_that_answered)
        if(self.input_that_answered == 0): # reception utm vehicule
            pass
        if(self.input_that_answered == 1): # reception angle euler
            pass
        if(self.input_that_answered == 2): # reception utm trajectoire
            liste_points.append(self.inputs["UTM_trajectoire"].ioelt.data)
            print("sampling")

    # destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        print(len(liste_points))
        pass
