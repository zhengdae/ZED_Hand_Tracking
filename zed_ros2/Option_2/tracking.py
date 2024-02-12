import mediapipe as mp
import cv2
import numpy as np
import matplotlib.pyplot as plt

class handtracking():
    def __init__(self, max_hands = 2,
                 detection_conf = 0.6,
                 tracking_conf = 0.9) -> None:
        self.mp_hands = mp.solutions.hands
        self.model = mp.solutions.hands.Hands(max_num_hands = max_hands, 
                                              min_detection_confidence = detection_conf, 
                                              min_tracking_confidence = tracking_conf)
        self.draw = mp.solutions.drawing_utils

    def detect_landmarks(self, image):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.model.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if self.results.multi_hand_landmarks:
            for landmarks in self.results.multi_hand_landmarks:
                self.draw.draw_landmarks(image, 
                                         landmarks, 
                                         self.mp_hands.HAND_CONNECTIONS)
        
        return image
    
    def plot(self, ax, plt, data, xlim=(-0.5, 0.5),ylim=(-0.5, 0.5),zlim=(0.2, 1.0)):
        if data.shape >= (21,3):
            ax.clear()
            ax.set_xlim3d(xlim)
            ax.set_ylim3d(ylim)
            ax.set_zlim3d(zlim)
            
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            
            ax.scatter3D(*zip(*data))

            edges = [(1,2),(2,3),(3,4),(0,5),(5,6),(5,9),(1,0),(6,7),(7,8),(0,9),(9,10),(10,11),(11,12),(9,13),(13,14),(14,15),(15,16),(13,17),(17,18),(18,19),(19,20),(0,17)]
            edges2 = [(22,23),(23,24),(24,25),(21,26),(26,27),(26,30),(22,21),(27,28),(28,29),(21,30),(30,31),(31,32),(32,33),(30,34),(34,35),(35,36),(36,37),(34,38),(38,39),(39,40),(40,41),(21,38)] 

            if data.shape != (42,3):
                for edge in edges:
                    ax.plot3D(*zip(data[edge[0]], data[edge[1]]), color='red')
            else:
                for edge in edges:
                    ax.plot3D(*zip(data[edge[0]], data[edge[1]]), color='red')
                for edge in edges2:
                    ax.plot3D(*zip(data[edge[0]], data[edge[1]]), color='blue')

            # Draw the plot
            plt.draw()
            plt.pause(0.0001)


    