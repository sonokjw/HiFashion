import cProfile
from turtle import window_width
import pygame
import pygame.camera
import pygame.image
from pygame.locals import *
import sys

import FitClothes
import Closet
import ChangeColor

pygame.init()
pygame.camera.init()

WIN_HEIGHT = 800
WIN_WIDTH = 1200

CAM_HEIGHT = WIN_HEIGHT * 3//4
CAM_WIDTH = WIN_WIDTH * 3 //4

IMAGE_SIZE = (350, 350)

NUM_CLOTHES = 2
NUM_COLOR = 1

# in case we want another number of clothes
if len(sys.argv) > 1:
    NUM_CLOTHES = int(sys.argv[1])


ended = False # whether app exited
person = False # whether a person is detected
clothes_i = 0 # index of current clothes in list

clothes = []
# load clothes
# transparent clothes: https://www.transparentpng.com/cats/shirt-1436.html
for i in range(NUM_CLOTHES):
    c = pygame.transform.scale(pygame.image.load(f'clothes/{i}.png'), IMAGE_SIZE)
    clothes.append(c)

class Button:
    def __init__(self, image, position, callback):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.callback = callback
 
    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self)
                
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("HiFashion")

# TODO: Kinect Camera
cam = pygame.camera.Camera("FaceTime HD Camera (Built-in)", (CAM_WIDTH, CAM_HEIGHT)) 

cam.start()
cam.set_controls(hflip = True, vflip = False)

pressing = False
cur_key = None

# app loop
while not ended:
    image = cam.get_image()
    win.blit(image, (0,0))

    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            ended = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        if not pressing:
            pressing = True
            cur_key = 'c'
    elif keys[pygame.K_LEFT]:
        if not pressing:
            pressing = True
            cur_key = 'left'
    elif pressing:
        pressing = False
        if cur_key == 'c':
            person = not person
            print('showing clothes:', person)
        elif cur_key == 'left' and person:
            clothes_i = (clothes_i+1) % len(clothes)
            print('next clothes')
    
            
    if person:
        win.blit(clothes[clothes_i], (400,150))
        
    pygame.display.update()
        
pygame.quit()
