import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
import csv

import utm

#conversion long/lat to UTM

class rtmaps_python(BaseComponent):
    #constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    #configuration des I/O
    def Dynamic(self):
        self.add_input("lat_long", rtmaps.types.ANY)
        self.add_output("UTM", rtmaps.types.FLOAT64);
        self.add_property("record_path", "C:/Users/bolo.LAPTOP-0A1UK5DI/Documents/ESIG/S8/repo git/records/record1/trajectoryCise.csv", rtmaps.types.FILE)
        self.add_property("recording", False)

    #appel a la creation
    def Birth(self):
        print("Converting to UTM")
        self.log = []

    #called every input
    def Core(self):
        entree = self.inputs["lat_long"].ioelt #on récupère l'entrée sous forme l'ioelt (voir doc)

        longitude = entree.data[1]
        latitude = entree.data[0]

        if (self.properties["recording"].data == True):
            self.log.append([latitude, longitude])

        utm_conversion = utm.from_latlon(latitude,longitude)
        Utmx = utm_conversion[0]
        Utmy = utm_conversion[1]

        self.outputs["UTM"].write([Utmx, Utmy]) #on envoie l'output sur la sortie du module

    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(") 
        print("UTM --> saving file")
        if (self.properties["recording"].data == True):
            with open(self.properties["record_path"].data, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerows(self.log)