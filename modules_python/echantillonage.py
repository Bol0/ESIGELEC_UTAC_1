import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
from rtmaps.base_component import BaseComponent
import pyproj  # in pyproj library there is a methdod called Geod
import csv
from scipy.interpolate import interp1d
import time

# the variables and there tasks

#data : the array with the original coordinates
# x = the length of the data array
#data2 : the numpy array of data
#y : the float type of data2
#x1 and y1 : the tuple arrays
#xi, yi : the arrays for all the points on the curve
#s : the length of the xi array
#data3 : all the points of the curve in one array

show_step2 = True  # to put the given coordinates to Book4.csv
show_step1 = False # to put the untreated coordinates to Book3.csv


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

        # to open the file( This csv file contains the untreated gps coordinates directly from the robot)
        with open(self.properties["path"].data) as csvDataFile:  # open the cvs file
            data = [row for row in csv.reader(csvDataFile, delimiter=';')]  # put it into and array [row][column]
            x = len(data)

        # to convert into a numpy array( array data to array data2)
        data2 = np.array(data)
        y = data2.astype(float)

        # to get the path curved path
        x1, y1 = zip(*y)  # return a tuple like array
        x1, y1 = y.T
        i = np.arange(len(y))

        # 1000x the original number of points
        interp_i = np.linspace(0, i.max(), 1000 * i.max())

        # break them down and put to two different arrays
        xi = interp1d(i, x1, kind='cubic')(interp_i)
        yi = interp1d(i, y1, kind='cubic')(interp_i)

        # the size of the xi coordinates
        s = len(xi)

        # write the new coordinates in the data3 array
        data3 = []  # the new coordinates which are on the curve(untreated)
        for m in range(s):
            data3.append([xi[m], yi[m]])

        if show_step1 == True:
            with open('Book3.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerows(data3)

        # The next part is to breakdown the given coordinates into 1m parts and give the treated coordinates

        # using that data to calculate the points where the distance is 1m
        wgs84_geod = pyproj.CRS('WGS 84').get_geod()  # this method is used to calculate the distance and the angle between the given points directly and it keeps updating giving us a fairly smooth curve

        result = []  # the result which is treated

        # The distance that we want the points to be( Here its 1 meter)
        delta = 1

        i = 0  # just a counter
        for k in range(1, s):
            latP1 = float(data3[i][0])
            lonP1 = float(data3[i][1])
            latP2 = float(data3[k][0])
            lonP2 = float(data3[k][1])

            if (i == 0) and (k == 1):
                # our current position
                lat, lon = latP1, lonP1
            while True:
                # keeps calculating the distance and the angle to make it smooth
                az, _, dist = wgs84_geod.inv(lon, lat, lonP2, latP2)  # the azimuth is the bearing. The angle between the points (https://pyproj4.github.io/pyproj/stable/api/geod.html)

                if dist > delta:
                    result.append([lat, lon])

                    lon, lat, _ = wgs84_geod.fwd(lon, lat, az, delta)  # create a point exactly after 1m and move to that point

                if dist == delta:
                    result.append([lat, lon])

                    i = i + 1
                    break

                if dist < delta:
                    break

        result.append([data[x - 1][0], data[x - 1][1]])
        # just to put the treated coordinates in the csv file
        if (self.properties["recording"].data):
            with open('ProcessedTrajectory.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerows(result)

        # send the output
        res_len = len(result)
        for j in range(res_len):
            self.outputs["points_traj"].write(result[j])
            print(result[j])
            time.sleep(0.01);
        exit(0)

    # destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass