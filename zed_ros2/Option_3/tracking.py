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
    
    def get_point_cloud(self, depth, u, v, fx, fy, cx, cy):
        X = (u - cx) * depth[v, u] / fx
        Y = (v - cy) * depth[v, u] / fy
        Z = depth[v, u]
        return X, Y, Z

    def get_position(self, image, depth, fx, fy, cx, cy, width, height):
        left_data = []
        right_data = []
        if self.results.multi_hand_landmarks:
            for num, landmarks in enumerate(self.results.multi_hand_landmarks):
                handedness = self.results.multi_handedness[self.results.multi_hand_landmarks.index(landmarks)].classification[0].label
                for id, landmark in enumerate(landmarks.landmark):
                    if id == 0:
                        wrist_landmark = [landmark.x, landmark.y, landmark.z]
                        X, Y = int(landmark.x * width), int(landmark.y * height)
                        if X > 0 and Y > 0:
                            wrist_x, wrist_y, wrist_z = self.get_point_cloud(depth, X, Y, fx, fy, cx, cy)

                    x_3d = wrist_x + (landmark.x * width - wrist_landmark[0] * width) * wrist_z/fx
                    y_3d = wrist_y + (landmark.y * height - wrist_landmark[1] * height) * wrist_z/fy
                    z_3d = wrist_z + (landmark.z - wrist_landmark[2]) * 2.1163 # 2.1163 is the focal length at VGA

                    hand_landmarks_3d = [x_3d, y_3d, z_3d]

                    if handedness == "Right":
                        left_data.append(hand_landmarks_3d)
                    elif handedness == "Left":
                        right_data.append(hand_landmarks_3d)

                if handedness == "Right":
                    cv2.putText(image, "Left", (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif handedness == "Left":
                    cv2.putText(image, "Right", (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        left_data = np.array(left_data)
        right_data = np.array(right_data)

        return left_data, right_data

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


    