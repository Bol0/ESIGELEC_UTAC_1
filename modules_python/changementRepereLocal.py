import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
import math
from rtmaps.base_component import BaseComponent
from scipy.spatial.transform import Rotation as R


class rtmaps_python(BaseComponent):

    #constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    #configuration des I/O
    def Dynamic(self):
        self.add_input("donnees", rtmaps.types.ANY)
        self.add_input("donnees_Traj", rtmaps.types.ANY)
        self.add_output("x_y", rtmaps.types.FLOAT64);
        self.add_property("distance_min", 0.5)

    #appel a la creation
    def Birth(self):
        print("starting...");
        self.trajectoire = []
        self.indexPosition = 0

    #called every input
    def Core(self):
        if(self.input_that_answered == 0): #entrée déclencé sur les données robot
            utmx=self.inputs["donnees"].ioelt.data[0]
            utmy=self.inputs["donnees"].ioelt.data[1]
            yaw=self.inputs["donnees"].ioelt.data[4] #A CHANGER TO 4 POUR LA VERSION FINALE 
        
            matricePassage = np.eye(4) #fait matrice identité 4x4

            #martice de passage
            translation = np.array([utmx,utmy,0]) #mettre le z a zero ? .59
            matricePassage[0:3,3]=translation
        
            rotation = R.from_euler('Z', [(3*math.pi/2)-yaw],degrees=False).as_matrix() # ajouter un offset au yaw et inverse la base
            matricePassage[0:3, 0:3] = rotation
            matricePassageInverse = np.linalg.inv(matricePassage) #matric inverse

            listedepointTraj = [] #liste contenant la trajectoire changé de base
            for i in range(len(self.trajectoire)):
                pointsTraj=np.array([self.trajectoire[i][0],self.trajectoire[i][1],0,1.0]) #X, Y et Z, et le 1 de la matrice identité
                produit = matricePassageInverse.dot(pointsTraj) # on fait le produit matriciel
                listedepointTraj.append([produit[0], produit[1]])
            if(self.indexPosition == len(listedepointTraj)) : #index a la fin de la liste, arret du robot, out of bounds
                self.outputs["x_y"].write([0,0])
            elif(math.sqrt(listedepointTraj[self.indexPosition][0]**2 + listedepointTraj[self.indexPosition][1]**2) < self.properties["distance_min"].data): #si la distance au point est inferieur a 0.5m
                self.indexPosition += 1
                print("passage au point suivant")
            else :
                #process distance for all points
                dist = []
                for i in range(len(listedepointTraj)):
                    dist.append(math.sqrt(listedepointTraj[i][0]**2 + listedepointTraj[i][1]**2))
                self.outputs["x_y"].write(listedepointTraj[self.indexPosition])
                print("point " + str(self.indexPosition))

        elif(self.input_that_answered == 1): #entrée déclenché sur la trajectoire
            #enregistrement des points
            #entree = self.inputs["donnees_Traj"].ioelt.data
            #np.append(self.trajectoire,entree)
            self.trajectoire.append([self.inputs["donnees_Traj"].ioelt.data[0],self.inputs["donnees_Traj"].ioelt.data[1]])

    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass 