import enum
import csv
from tkinter import N
import pygame
'''
All the constants, helpful functions or classes here
'''

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

DISPLAY_SIZE = 250
LABEL_LOC = (480, 50)
LABEL_LOC2 = (520, 50)
LABEL_LOC3 = (520, 500)
MUTED_WHITE = (249, 245, 236)
MUTED_BLACK = (18,18,18)
X = 50  # horizontal starting point
Y = 150 # vertical starting point
DIST = 25 # distance between images


# all possible pages of apps
class Modes(enum.Enum):
    HOME = 1
    CLOSET = 2
    FAV = 3

# all clothes types
class ClothType(enum.Enum):
    UPPER = 1
    LOWER = 2

# Clothes dic with shoulder or hip width data
cloth_dic = {}

file = open('clothes/ClothData.csv')
csvreader = csv.reader(file)
header = []
header = next(csvreader)
for row in csvreader:
    ind = int(row[0])
    cloth_dic[ind] = {}
    for i in range(1, len(header)):
        metric = header[i]
        if 'margin' in metric:
            cloth_dic[ind][metric] = float(row[i])
        elif metric == 'ctype':
            if  'Top' in row[i]:
                cloth_dic[ind][metric] = ClothType.UPPER
            elif 'Bottom' in row[i]:
                cloth_dic[ind][metric] = ClothType.LOWER


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
    
    def show(self, win):
        if self.hovering:
            win.blit(self.images[1], self.pos)
        else:
            win.blit(self.images[0], self.pos)
 
    def change_mode(self, cur_mode):
        # if self.mode is None:
        #     return cur_mode, False

        if cur_mode == self.mode:
            print("Current mode:", cur_mode)
            return Modes.HOME, False

        print("Current mode:", cur_mode)
        return self.mode, True

    def on_click(self, event, cur_mode):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    return self.change_mode(cur_mode=cur_mode)
            self.hovering = True
        else:
            self.hovering = False
        return None, False


'''
cloth: the selected cloth image [front, back]
ind: the index of the cloth in cloth_dic
position: (x, y) coordinates of top-left of button
selected: if the cloth is slescted
'''
class Hanger:
    def __init__(self, position, cloth, ind):
        self.pos = position
        self.selected = False
        self.cloth = cloth
        self.ind = ind
        self.prev = 0 
        self.hovering = 0
        self.rect = cloth[self.hovering].get_rect(topleft=position)
        # print(self.ind,": ", len(self.cloth))
    
    def setPos(self, pos):
        self.pos = pos
        self.rect = self.cloth[self.hovering].get_rect(topleft=pos)

    def show(self, win):
        width = self.cloth[self.hovering].get_width()
        height = self.cloth[self.hovering].get_height()
        if self.selected:
            pygame.draw.rect(self.cloth[self.hovering], AQUA, [0, 0, width, height], 1)
        else:
            pygame.draw.rect(self.cloth[self.hovering], MUTED_WHITE, [0, 0, width, height], 1)
        
        if len(self.cloth) == 2:
            # print("!!!!!!!!!!!!!!!!!!hovering!!!!!!!!!!!!",self.hovering)
            win.blit(self.cloth[self.hovering], self.pos)
        else:
            win.blit(self.cloth[0], self.pos)

    def on_click(self, event):
        # print("~~~~~~~~~~~~~~~~getting on click ~~~~~~~~~~", event)
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            # print("collided????????????")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.selected = not self.selected
            self.prev = self.hovering
            if len(self.cloth) > 1:
                self.hovering = 1
                return True
        else:
            self.prev = self.hovering
            self.hovering = 0
        return self.prev != self.hovering

    

'''
Load clothes from the clothes directory
return: dict 
            key: clothes index
            val: [front, back(optional)]
'''
def load_clothes():
    clothes = {}
    i = 0

    # load clothes front images
    while True:
        try:
            img = pygame.image.load(f'clothes/{i}.png')
            dim = (IMAGE_WIDTH, int(float(img.get_height())/img.get_width()*IMAGE_WIDTH))
            c = pygame.transform.scale(img, dim)
            clothes[i] = [c]
        except:
            break
        i += 1
    # load clothes back images if exists
    for j in range(i):
        try:
            img = pygame.image.load(f'clothes/{j}b.png')
            dim = (IMAGE_WIDTH, int(float(img.get_height())/img.get_width()*IMAGE_WIDTH))
            c = pygame.transform.scale(img, dim)
            clothes[j].append(c)
        except:
            pass
    
    return clothes


# Back and Next buttons
left_icon = pygame.transform.scale(pygame.image.load("icons/left.png"), (int(ICON_SIZE[0]/1.5), int(ICON_SIZE[1]/1.5)))
left_icon_hover = pygame.transform.scale(pygame.image.load("icons/left.png"), (int(ICON_SIZE[0]/1.5), int(ICON_SIZE[1]/1.5)))
left_icon_hover.fill((DARKEN, DARKEN, DARKEN), special_flags=pygame.BLEND_RGB_SUB)

right_icon = pygame.transform.scale(pygame.image.load("icons/right.png"), (int(ICON_SIZE[0]/1.5), int(ICON_SIZE[1]/1.5)))
right_icon_hover = pygame.transform.scale(pygame.image.load("icons/right.png"), (int(ICON_SIZE[0]/1.5), int(ICON_SIZE[1]/1.5)))
right_icon_hover.fill((DARKEN, DARKEN, DARKEN), special_flags=pygame.BLEND_RGB_SUB)

left_btn = Button([left_icon, left_icon_hover], (5, WIN_HEIGHT//2 + 50), None)
right_btn = Button([right_icon, right_icon_hover], (WIN_WIDTH - 80, WIN_HEIGHT//2 + 50), None)

fav_left_btn = Button([left_icon, left_icon_hover], (5, WIN_HEIGHT//2 - 260), None)
fav_right_btn = Button([right_icon, right_icon_hover], (WIN_WIDTH - 80, WIN_HEIGHT//2 - 260), None)