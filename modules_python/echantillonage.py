import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
import pyproj   #in pyproj library there is a methdod called Geod

class rtmaps_python(BaseComponent):
    #constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    #configuration des I/O
    def Dynamic(self):
        self.add_input("latP", rtmaps.types.ANY)
        self.add_input("lonP", rtmaps.types.ANY)
        self.add_input("latR", rtmaps.types.ANY)
        self.add_input("lonR", rtmaps.types.ANY)
        self.add_output("points_traj", rtmaps.types.AUTO);

    #appel a la creation
    def Birth(self):
        print("starting...");

    #called every input
    def Core(self):

        # WGS-84 is the coordinate system used by GPS
        wgs84_geod = pyproj.CRS('WGS 84').get_geod()  # this method is used to calculate the distance and the angle between the given points directly and it keeps updating giving us a fairly smooth curve

        # The distance that we want the points to be( Here its 1 meter)
        delta = 1

        # our current position
        lat, lon = self.input["latR"], self.input["lonR"]
        points_traj = []

        while True:
            # keeps calculating the distance and the angle to make it smooth
            az, _, dist = wgs84_geod.inv(lon, lat, self.input["lonR"], self.input["latP"])  # the azimuth is the bearing. The angle between the points (https://pyproj4.github.io/pyproj/stable/api/geod.html)

            # if the distance is less than 1 meter
            if dist < delta:
                break

            points_traj.append((lat, lon))

            # moving from point to point towards our last point
            lon, lat, _ = wgs84_geod.fwd(lon, lat, az, delta)


        self.outputs["points_traj"].write(points_traj)


    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass