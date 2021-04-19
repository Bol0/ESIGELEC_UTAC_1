import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent

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
        self.add_input("angle_erreur", rtmaps.types.ANY)
        self.add_input("distance", rtmaps.types.ANY)
        self.add_output("vitesse_laterale", rtmaps.types.AUTO)
        self.add_output("vitesse_longitudinale", rtmaps.types.AUTO);

    #appel a la creation
    def Birth(self):
        print("starting...");

    #called every input
    def Core(self):
        angle=self.inputs["angle_erreur"].ioelt
        distance=self.inputs["distance"].ioelt

        #on calcule la vitesse
        distance_points = 1 #distance entres les points échantillonées en m
        vitesse_max = 4 #vitesse map en sortie en m/s
        vitesse_norme = (distance/distance_points)*vitesse_max
        if(vitesse_norme > vitesse_max): #si la norme de vitesse depasse la vitesse max, on la sature
            vitesse_norme = vitesse_max
        

        vit_long = vitesse_norme*sin(angle)
        vit_lat = vitesse_norme*cos(angle)
        
        self.outputs["vitesse_laterale"].write(Utmx)
        self.outputs["vitesse_longitudinale"].write(Utmx)



    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass