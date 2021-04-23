import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
import math

#script simple
#on crée une entrée et une sortie
#on moyenne l'entrée sur 10 échantillons
#on envoie le résultat a la sortie

class rtmaps_python(BaseComponent):
    #constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

        self.q1 = [0] #on init la file
        for i in range(1, 11):
            self.q1.append(i)

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
        distance_points = 1 #distance entres les points échantillonées en m
        vitesse_max = 1 #vitesse map en sortie en m/s
        vitesse_norme = (distance/distance_points)*vitesse_max
        if(vitesse_norme > vitesse_max): #si la norme de vitesse depasse la vitesse max, on la sature
            vitesse_norme = vitesse_max
        

        vit_long = vitesse_norme
        vit_lat = 1*angle

        if(obstacle == 1):#arret du robot
            vit_long = 0
            vit_lat = 0
        
        self.outputs["vitesse_laterale"].write(float(vit_lat))
        self.outputs["vitesse_longitudinale"].write(float(vit_long))



    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass