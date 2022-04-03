import cProfile

from turtle import window_width
import pygame
import pygame.camera
import pygame.image
from pygame.locals import *
import sys
import enum

import FitClothes
import Closet
import ChangeColor

pygame.init()
pygame.camera.init()

# defining constants
WIN_HEIGHT = 700
WIN_WIDTH = 1200

CAM_HEIGHT = WIN_HEIGHT * 3//4
CAM_WIDTH = WIN_WIDTH * 3 //4

IMAGE_SIZE = (350, 350)
ICON_SIZE = (75, 75)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("HiFashion")

# all possible pages of apps
class Modes(enum.Enum):
    HOME = 1
    CLOSET = 2
    FAV = 3

cur_mode = Modes.HOME

ended = False # whether app exited
person = False # whether a person is detected
clothes_i = 0 # index of current clothes in list

clothes = []
# load clothes
# transparent clothes: https://www.transparentpng.com/cats/shirt-1436.html
i = 0
while True:
    try:
        c = pygame.transform.scale(pygame.image.load(f'clothes/{i}.png'), IMAGE_SIZE)
        clothes.append(c)
    except:
        break
    i += 1

NUM_CLOTHES = i
NUM_COLOR = 1

# in case we want another number of clothes
if len(sys.argv) > 1:
    NUM_CLOTHES = min(NUM_CLOTHES, int(sys.argv[1]))

class Button:
    def __init__(self, image, position, mode):
        self.image = image
        self.mode = mode
        self.rect = image.get_rect(topleft=position)
    
    def show(self):
        win.blit(self.image, self.rect)
 
    def change_mode(self):
        print(f'button {self.mode} clicked: {cur_mode}')
        # if cur_mode == self.mode:
        #     cur_mode = Modes.HOME
        # else:
        #     cur_mode = self.mode

    def on_click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_mode()



# TODO: Kinect Camera
cam = pygame.camera.Camera("FaceTime HD Camera (Built-in)", (CAM_WIDTH, CAM_HEIGHT))

cam.start()
cam.set_controls(hflip = True, vflip = False)

closet_icon = pygame.transform.scale(pygame.image.load("icons/closet.png"), ICON_SIZE)
fav_icon = pygame.transform.scale(pygame.image.load("icons/fav.png"), ICON_SIZE)
closet_btn = Button(closet_icon, (WIN_WIDTH-100, WIN_HEIGHT-100), Modes.CLOSET)
fav_btn = Button(fav_icon, (25, WIN_HEIGHT-100), Modes.FAV)

pressing = False
cur_key = None

# app loop
while not ended:
    image = cam.get_image()
    win.blit(image, (0,0))

    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            ended = True
        closet_btn.on_click(event)
        fav_btn.on_click(event)

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
        clothes[clothes_i] = FitClothes.fitclothes(clothes[clothes_i])
        win.blit(clothes[clothes_i], (400,150))

    closet_btn.show()
    fav_btn.show()
    
    pygame.display.update()
        
pygame.quit()
