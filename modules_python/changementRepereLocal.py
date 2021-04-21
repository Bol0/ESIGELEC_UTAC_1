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

        self.q1 = [0] #on init la file
        for i in range(1, 15):
            self.q1.append(i)

    #configuration des I/O
    def Dynamic(self):
        self.add_input("donnees", rtmaps.types.ANY)
        self.add_input("donnees_Traj", rtmaps.types.ANY)
        self.add_output("liste_points_Traj", rtmaps.types.AUTO)
        self.add_output("liste_points", rtmaps.types.AUTO);

    #appel a la creation
    def Birth(self):
        print("starting...");

    #called every input
    def Core(self):
        utmx=self.inputs["donnees"].ioelt.data[0]
        utmy=self.inputs["donnees"].ioelt.data[1]
        yaw=self.inputs["donnees"].ioelt.data[4]
        utmxTraj=self.inputs["donnees_Traj"].ioelt.data[0]
        utmyTraj=self.inputs["donnees_Traj"].ioelt.data[1]
        utmzTraj=self.inputs["donnees_Traj"].ioelt.data[2]
        
        H= np.eye(4)#faite matrice 4x4
        
        #martice de passage
        translation = np.array([utmx,utmy,0])
        H[0:3,3]=translation
        
        rMatrix = R.from_euler("ZYX",np.array([math.pi/2.0-yaw,0,0]),degrees=False).as_matrix() # [math.pi/2.0-yaw] a remplacer
        H[0:3, 0:3] = rMatrix
        
        
        Hinv=np.linalg.inv(H)
        #transfer des coordonnees robot dans le repère local du robot
        listedepointRobot=[]
        
        pointsRobot=np.array([utmx,utmy,0,1.0])
        
        H2=Hinv.dot(pointsRobot)
        listedepointRobot.append(H2[0])
        listedepointRobot.append(H2[1])
        listedepointRobot.append(H2[2])
        
        #transfer des coordonnes de la traj dans le repere local du robot
        listedepointTraj=[]
        pointsTraj=np.array([utmxTraj,utmyTraj,utmzTraj,1.0])
        
        H3=Hinv.dot(pointsTraj)
        listedepointTraj.append(H3[0])
        listedepointTraj.append(H3[1])
        listedepointTraj.append(H3[2])
        
        self.outputs["liste_points"].write(listedepointRobot)
        self.outputs["liste_points_Traj"].write(listedepointTraj)

    #destroy
    def Death(self):
        print("         Why did you kill me !??        :'(");
        pass