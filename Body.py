from tracemalloc import start
import mediapipe as mp
import pygame.image
import pygame.draw
import numpy as np

'''
Tracks the body of the user, if in sight
'''

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

GRAY = (192, 192, 192)
RED = (220,20,60)
BLUE = (0,191,255)
BG_COLOR = GRAY
STROKE = 3

class Body:
    def __init__(self, win_w, win_h):
        self.locations = [None]*4
        self.screen_dim = (win_w, win_h)

    def track(self, img):
        self.locations = [(-1, -1)]*4

        with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5
        ) as pose:
            
            #  create a copy of the surface
            view = pygame.surfarray.array3d(img)

            #  convert from (width, height, channel) to (height, width, channel)
            view = view.transpose([1, 0, 2])

            # compute results
            results = pose.process(view)

            if results.pose_landmarks:
                # get desired to-scale coordinates
                # Note: since we are having webcams, it's reversed
                right_shoulder = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * img.get_width(),\
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * img.get_height())
                left_shoulder = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * img.get_width(),\
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * img.get_height())
                right_hip = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * img.get_width(),\
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * img.get_height())
                left_hip = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * img.get_width(),\
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * img.get_height())
                self.locations = [self.in_sight(left_shoulder), self.in_sight(right_shoulder), self.in_sight(left_hip), self.in_sight(right_hip)]

        # print(locations)
        return self.locations
        
    '''
    check whether coor is within the boundary of the screen

    return: coor if in-sight, else None
    '''
    def in_sight(self, coor):
        if 0 <= coor[0] <= self.screen_dim[0] and 0 <= coor[1] <= self.screen_dim[1]:
            return coor
        return None

    def draw(self, win):
        if self.locations[0] and self.locations[1]:
            pygame.draw.line(win, RED, self.locations[0], self.locations[1], STROKE)
        if self.locations[2] and self.locations[3]:
            pygame.draw.line(win, BLUE, self.locations[2], self.locations[3], STROKE)