import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
import pyproj  # in pyproj library there is a methdod called Geod
import csv

log = True
path = "C:/Users/bolo.LAPTOP-0A1UK5DI/Documents/ESIG/S8/repo git/records/record1/trajectoryCise.csv"

class rtmaps_python(BaseComponent):
    # constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    # configuration des I/O
    def Dynamic(self):

        self.add_output("points_traj", rtmaps.types.AUTO);

    # appel a la creation
    def Birth(self):
        print("starting...");

    # called every input
    def Core(self):

        with open(path) as csvDataFile:  # open the cvs file
            data = [row for row in csv.reader(csvDataFile, delimiter=';')]  # put it into and array [row][column]
            x = len(data)
            # print("x =" +str(x))
            # print(data[0][1])
        show = True
        # WGS-84 is the coordinate system used by GPS
        wgs84_geod = pyproj.CRS('WGS 84').get_geod()  # this method is used to calculate the distance and the angle between the given points directly and it keeps updating giving us a fairly smooth curve
        i = 1
        k = 1
        result = []

        # The distance that we want the points to be( Here its 1 meter)
        delta = 1

        while (k < x):

            latP1 = data[i - 1][0]
            lonP1 = data[i - 1][1]
            latP2 = data[k][0]
            lonP2 = data[k][1]

            if (i == 1):
                # our current position
                lat, lon = latP1, lonP1

            # keeps calculating the distance and the angle to make it smooth
            az, _, dist = wgs84_geod.inv(lon, lat, lonP2, latP2)  # the azimuth is the bearing. The angle between the points (https://pyproj4.github.io/pyproj/stable/api/geod.html)

            if dist == delta:  # if its equal put the starting coordinates on the list and come out of the while loop
                result.append((lat, lon))

            if dist > delta:  # if the distance greater than 1m, put the starting coordinates on the list, then move to another set of coordinates which are located in 1m
                while (True):
                    result.append((lat, lon))
                    lon, lat, _ = wgs84_geod.fwd(lon, lat, az,
                                                 delta)  # create a point exactly after 1m and move to that point
                    az, _, dist = wgs84_geod.inv(lon, lat, lonP2, latP2)

                    if dist == delta:
                        break

                    if dist < delta:
                        break
            # if the distance is less than 1 meter
            if dist < delta:
                k = k+1

            i = i + 1
            k = k + 1



        if (log == True):
            with open('Book1.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerows(result)

        y = len(result)
        for j in range(y):
            self.outputs["points_traj"].write(result[j])
        exit(0)

    # destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass