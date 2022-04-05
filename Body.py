from tracemalloc import start
# import cv2
import mediapipe as mp
import pygame.image
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

GRAY = (192, 192, 192)
BG_COLOR = GRAY

class Body:
    def __init__(self):
        pass

    def track(self, img):
        locations = [(-1, -1)]*4

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
                # # HOW U GET COORDINATES HERE
                # print(
                #     f'Left shoulder coordinates: ('
                #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * img.get_width()}, '
                #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * img.get_height()})'
                # )

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
                locations = [left_shoulder, right_shoulder, left_hip, right_hip]

        # print(locations)
            
        return locations
        
    def draw(self):
        pass