from turtle import window_width
import pygame
import pygame.camera
from pygame.locals import *
import sys

pygame.init()
pygame.camera.init()

WIN_HEIGHT = 1200
WIN_WIDTH = 1200

CAM_HEIGHT = WIN_HEIGHT * 3// 4
CAM_WIDTH = WIN_WIDTH * 3 //4

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("HiFashion")

# TODO: Kinect Camera
cam = pygame.camera.Camera("FaceTime HD Camera (Built-in)", (CAM_WIDTH, CAM_HEIGHT)) 

cam.start()
cam.set_controls(hflip = True, vflip = False)

ended = False

while not ended:
    image = cam.get_image()
    win.blit(image, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            ended = True

pygame.quit()