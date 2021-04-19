import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent

import utm

#conversion long/lat to UTM

class rtmaps_python(BaseComponent):
    #constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    #configuration des I/O
    def Dynamic(self):
        self.add_input("long_lat", rtmaps.types.ANY)
        self.add_output("UTMx", rtmaps.types.AUTO);
        self.add_output("UTMy", rtmaps.types.AUTO);

    #appel a la creation
    def Birth(self):
        print("Converting to UTM")

    #called every input
    def Core(self):
        entree = self.inputs["long_lat"].ioelt #on récupère l'entrée sous forme l'ioelt (voir doc)

        longitude = entree.data[1]
        latitude = entree.data[0]

        utm_conversion = utm.from_latlon(latitude,longitude)
        Utmx = utm_conversion[0]
        Utmy = utm_conversion[1]

        self.outputs["UTMx"].write(Utmx) #on envoie l'output sur la sortie du module
        self.outputs["UTMy"].write(Utmy)

    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(") 