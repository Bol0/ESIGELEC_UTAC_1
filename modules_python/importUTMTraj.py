import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
import pyproj  # in pyproj library there is a methdod called Geod
import csv

log = False

class rtmaps_python(BaseComponent):
    # constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    # configuration des I/O
    def Dynamic(self):
        self.add_output("points_traj", rtmaps.types.FLOAT64);
        self.add_property("path", "C:/Users/bolo.LAPTOP-0A1UK5DI/Documents/ESIG/S8/repo git/records/record1/trajectoryCise.csv", rtmaps.types.FILE)
        self.add_property("recording", False)

    # appel a la creation
    def Birth(self):
        print("starting...");

    # called every input
    def Core(self):

        with open(self.properties["path"].data) as csvDataFile:  # open the cvs file
            data = [row for row in csv.reader(csvDataFile, delimiter=' ')]  # put it into and array [row][column]
            x = len(data)

        for j in range(len(data)):
            out = data[j]
            print(out)
            self.outputs["points_traj"].write([float(out[0]), float(out[1])])

        exit(0)



    # destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass