import rtmaps.types
import numpy as np
import rtmaps.core as rt
import rtmaps.reading_policy
import math
from rtmaps.base_component import BaseComponent
from scipy.spatial.transform import Rotation as R

trajectoire = []
indexPosition = 0

class rtmaps_python(BaseComponent):
    #constructeur de la classe
    def __init__(self):
        BaseComponent.__init__(self)

    #configuration des I/O
    def Dynamic(self):
        self.add_input("donnees", rtmaps.types.ANY)
        self.add_input("donnees_Traj", rtmaps.types.ANY)
        #self.add_output("liste_points_Traj", rtmaps.types.AUTO)
        self.add_output("x_y", rtmaps.types.AUTO);

    #appel a la creation
    def Birth(self):
        print("starting...");
        trajectoire = []
        indexPosition = 0

    #called every input
    def Core(self):
        global indexPosition
        if(self.input_that_answered == 0): #entrée déclencé sur les données robot
            utmx=self.inputs["donnees"].ioelt.data[0]
            utmy=self.inputs["donnees"].ioelt.data[1]
            yaw=self.inputs["donnees"].ioelt.data[4]
        
            H= np.eye(4)#faite matrice 4x4
        
            #martice de passage
            translation = np.array([utmx,utmy,0])
            H[0:3,3]=translation
        
            rMatrix = R.from_euler("ZYX",np.array([math.pi/2.0-yaw,0,0]),degrees=False).as_matrix() # [math.pi/2.0-yaw] a remplacer
            H[0:3, 0:3] = rMatrix
            
            Hinv=np.linalg.inv(H)
            #transfer des coordonnees robot dans le repère local du robot
            #listedepointRobot=[]
            
            #pointsRobot=np.array([utmx,utmy,0,1.0])
            
            #H2=Hinv.dot(pointsRobot)
            #listedepointRobot.append(H2[0])
            #listedepointRobot.append(H2[1])
            #listedepointRobot.append(H2[2])
            
            #transfer des coordonnes de la traj dans le repere local du robot
            listedepointTraj=[]
            for i in range(len(trajectoire)):
                pointsTraj=np.array([trajectoire[i][0],trajectoire[i][1],1.0,1.0])
            
                H3=Hinv.dot(pointsTraj)
                listedepointTraj.append([H3[0], H3[1]])
        
            #self.outputs["liste_points"].write(listedepointRobot)
            if(math.sqrt(listedepointTraj[indexPosition][0]**2+ listedepointTraj[indexPosition][1]**2) < 0.5):
                indexPosition += 1
                print("passage au point suivant")
            elif(indexPosition == len(listedepointTraj)-1) :
                self.outputs["x_y"].write([0,0])
            else :
                self.outputs["x_y"].write(listedepointTraj[indexPosition])
                #self.outputs["x_y"].write(listedepointTraj[0])

        elif(self.input_that_answered == 1): #entrée déclenché sur la trajectoire
            #enregistrement des points
            trajectoire.append(self.inputs["donnees_Traj"].ioelt.data)

    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass