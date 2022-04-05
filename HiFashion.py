import pygame
import pygame.camera
import pygame.image
import sys
import enum

from FitClothes import fitClothes
from ChangeColor import *

from Home import Home
from Fav import Fav
from Closet import Closet

# defining constants
WIN_HEIGHT = 700
WIN_WIDTH = 1200
WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)

CAM_HEIGHT = WIN_HEIGHT * 3//4
CAM_WIDTH = WIN_WIDTH * 3 //4
CAM_SIZE = (CAM_WIDTH, CAM_HEIGHT)

IMAGE_WIDTH = 350
ICON_SIZE = (75, 75)

# Morandi color coding
RED_VINE = (186, 73, 76)
MATCHA = (199, 199, 187)
AQUA = (95, 120, 128)
SUN_KISSED = (20, 38, 48)
MORANDI = [RED_VINE, MATCHA, AQUA, SUN_KISSED]
MUTED_WHITE = (249, 245, 236)
MUTED_BLACK = (18,18,18)

DARKEN = 30 # how much to darken the button when hovering

# all possible pages of apps
class Modes(enum.Enum):
    HOME = 1
    CLOSET = 2
    FAV = 3

cur_mode = Modes.HOME # current screen of app
ended = False # whether app exited

# Load Clothes
# transparent clothes: https://www.transparentpng.com/cats/shirt-1436.html
clothes = []
i = 0
while True:
    try:
        img = pygame.image.load(f'clothes/{i}.png')
        dim = (IMAGE_WIDTH, int(float(img.get_height())/img.get_width()*IMAGE_WIDTH))
        c = pygame.transform.scale(img, dim)
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
            print("Current mode:", cur_mode)
            return False
        
        cur_mode = self.mode
        print("Current mode:", cur_mode)
        return True

    def on_click(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    return self.change_mode()
            self.hovering = True
        else:
            self.hovering = False
        return False


# App Display Setup
pygame.init()
pygame.camera.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("HiFashion")

# TODO: Kinect Camera
user_cam = pygame.camera.list_cameras()[0]
cam = pygame.camera.Camera(user_cam, (CAM_WIDTH, CAM_HEIGHT))
cam.start()
cam.set_controls(hflip = True, vflip = False)

# Text Setup
font = pygame.font.SysFont("helvetica", 48)

# Button Setup
closet_icon = pygame.transform.scale(pygame.image.load("icons/closet.png"), ICON_SIZE)
closet_icon_hover = pygame.transform.scale(pygame.image.load("icons/closet.png"), ICON_SIZE)
closet_icon_hover.fill((DARKEN, DARKEN, DARKEN), special_flags=pygame.BLEND_RGB_SUB)

fav_icon = pygame.transform.scale(pygame.image.load("icons/fav.png"), ICON_SIZE)
fav_icon_hover = pygame.transform.scale(pygame.image.load("icons/fav.png"), ICON_SIZE)
fav_icon_hover.fill((DARKEN, DARKEN, DARKEN), special_flags=pygame.BLEND_RGB_SUB)

closet_btn = Button([closet_icon, closet_icon_hover], (WIN_WIDTH-100, WIN_HEIGHT-100), Modes.CLOSET)
fav_btn = Button([fav_icon, fav_icon_hover], (25, WIN_HEIGHT-100), Modes.FAV)

# App pages Setup
home_pg = Home(NUM_CLOTHES)
closet_pg = Closet(win, clothes, font)
fav_pg = Fav(win, font)

new_clothes = {} # a dictionary saving new clothing colors based on color scheme

########### App Loop ###########
while not ended:
    # buttons or quit events
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            ended = True
        if cur_mode != Modes.FAV:
            change = closet_btn.on_click(event)
            if change:
                closet_pg.to_closet()
        if cur_mode != Modes.CLOSET:
            change = fav_btn.on_click(event)
            if change:
                fav_pg.to_fav()
    
    # update current page
    if cur_mode == Modes.HOME:
        image = cam.get_image()
        win.blit(image, (0,0))
        person, clothes_i, screenshot = home_pg.update()
        if person:
            cloth = clothes[clothes_i]
            # change color
            ind = home_pg.color % (len(MORANDI) + 1)
            if clothes_i not in new_clothes:
                new_clothes[clothes_i] = [cloth]
                for color in MORANDI:
                    # print("Morandi color: ", color)
                    new_clothes[clothes_i].append(change_color(cloth, color))
            cloth = new_clothes[clothes_i][ind]
            clothes[clothes_i] = fitClothes(cloth)
            win.blit(cloth, (400,150))
        if screenshot:
            fav_pg.saveOutfit(win)
    elif cur_mode == Modes.CLOSET:
        closet_pg.update()
    else: # Fav
        fav_pg.update()

    # update button display
    if cur_mode != Modes.FAV:
        closet_btn.show()
    if cur_mode != Modes.CLOSET:
        fav_btn.show()
    
    pygame.display.update()
        
pygame.quit()