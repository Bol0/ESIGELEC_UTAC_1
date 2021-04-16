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
        self.add_input("coordsFiltre", rtmaps.types.ANY)
        self.add_input("pointsTraj", rtmaps.types.ANY)
        self.add_output("angleErreur", rtmaps.types.AUTO);

    #appel a la creation
    def Birth(self):
        print("starting...");

    #called every input
    def Core(self):
        latitude=self.inputs["Latitude"].ioelt
        longitude=self.inputs["Longitude"].ioelt
        
        self.q1.append(latitude.data) #on ajoute l'entrée a la fin de la file
        self.q1.pop(0)
        
        self.q2.append(longitude.data) #on ajoute l'entrée a la fin de la file
        self.q2.pop(0)
        
        utm_conversion = utm.from_latlon(latitude,longitude)
        Utmx= utm_conversion [0]
        Utmy= utm_conversion [1]
        
        self.outputs["pointsTraj"].write(Utmx)


    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass