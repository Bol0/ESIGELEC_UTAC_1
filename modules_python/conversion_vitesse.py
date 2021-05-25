import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
import math

#script de convertion entre distance et angle d'erreur vers vitesse longi/lat

class rtmaps_python(BaseComponent):
    #constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    #configuration des I/O
    def Dynamic(self):
        self.add_input("angle_distance", rtmaps.types.ANY)
        self.add_input("isObstacle", rtmaps.types.ANY)
        self.add_output("vitesse_laterale", rtmaps.types.FLOAT64)
        self.add_output("vitesse_longitudinale", rtmaps.types.FLOAT64);

    #appel a la creation
    def Birth(self):
        print("starting...");

    #called every input
    def Core(self):
        in1 = self.inputs["angle_distance"].ioelt
        angle = in1.data[0]
        distance = in1.data[1]
        if("isObstacle" in self.inputs):
            obstacle = self.inputs["isObstacle"].ioelt.data
        else:
            obstacle = 0

        #on calcule la vitesse
        vitesse_long = 1 #vitesse longitudinale de base en m/s
        vitesse_lat = 2*angle #max 2 ou 3 rad
        
        
        if (vitesse_lat >= 1):
            vitesse_long = vitesse_long/(abs(vitesse_lat)*1)
            
        if(obstacle == 1):#arret du robot
        
            vitesse_long = 0
            vitesse_lat = 0
        
        self.outputs["vitesse_laterale"].write(float(vitesse_lat))
        self.outputs["vitesse_longitudinale"].write(float(vitesse_long))



    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass