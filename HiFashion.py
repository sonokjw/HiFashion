import cProfile
from glob import glob

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

# defining constants
WIN_HEIGHT = 700
WIN_WIDTH = 1200

CAM_HEIGHT = WIN_HEIGHT * 3//4
CAM_WIDTH = WIN_WIDTH * 3 //4

IMAGE_SIZE = (350, 350)
ICON_SIZE = (75, 75)

DARKEN = 30 # how much to darken the button when hovering

# all possible pages of apps
class Modes(enum.Enum):
    HOME = 1
    CLOSET = 2
    FAV = 3

cur_mode = Modes.HOME # current screen of app
ended = False # whether app exited
person = False # whether a person is detected
clothes_i = 0 # index of current clothes in list

# Load Clothes
# transparent clothes: https://www.transparentpng.com/cats/shirt-1436.html
clothes = []
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

'''
images: [icon, icon_hover] a list of two icon images
position: (x, y) coordinates of top-left of button
mode: Modes mode to be changed when this button is clicked
'''
class Button:
    def __init__(self, images, position, mode):
        self.images = images
        self.mode = mode
        self.pos = position
        self.rect = images[0].get_rect(topleft=position)
        self.hovering = False
    
    def show(self):
        global win
        if self.hovering:
            win.blit(self.images[1], self.pos)
        else:
            win.blit(self.images[0], self.pos)
 
    def change_mode(self):
        global cur_mode
        if cur_mode == self.mode:
            cur_mode = Modes.HOME
        else:
            cur_mode = self.mode

    def on_click(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.change_mode()
            self.hovering = True
        else:
            self.hovering = False


# App Display Setup
pygame.init()
pygame.camera.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("HiFashion")

# TODO: Kinect Camera
cam = pygame.camera.Camera("FaceTime HD Camera (Built-in)", (CAM_WIDTH, CAM_HEIGHT))
cam.start()
cam.set_controls(hflip = True, vflip = False)

# Button Setup
closet_icon = pygame.transform.scale(pygame.image.load("icons/closet.png"), ICON_SIZE)
closet_icon_hover = pygame.transform.scale(pygame.image.load("icons/closet.png"), ICON_SIZE)
closet_icon_hover.fill((DARKEN, DARKEN, DARKEN), special_flags=pygame.BLEND_RGB_SUB)

fav_icon = pygame.transform.scale(pygame.image.load("icons/fav.png"), ICON_SIZE)
fav_icon_hover = pygame.transform.scale(pygame.image.load("icons/fav.png"), ICON_SIZE)
fav_icon_hover.fill((DARKEN, DARKEN, DARKEN), special_flags=pygame.BLEND_RGB_SUB)

closet_btn = Button([closet_icon, closet_icon_hover], (WIN_WIDTH-100, WIN_HEIGHT-100), Modes.CLOSET)
fav_btn = Button([fav_icon, fav_icon_hover], (25, WIN_HEIGHT-100), Modes.FAV)

# Key Press Detection Setup
pressing = False
cur_key = None


########### App Loop ###########
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