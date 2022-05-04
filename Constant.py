import enum
import csv
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
cloth: the selected cloth image
ind: the index of the cloth in cloth_dic
position: (x, y) coordinates of top-left of button
selected: if the cloth is slescted
'''
class Hanger:
    def __init___(self, position, cloth, ind):
        self.pos = position
        self.selected = False
        self.cloth = cloth
        self.ind = ind
        self.rect = cloth.get_rect(topleft=position)

    def show(self, win):
        if self.selected:
            win.blit(self.cloth, self.pos)
    

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
            img = pygame.image.load(f'clothes/{i}b.png')
            dim = (IMAGE_WIDTH, int(float(img.get_height())/img.get_width()*IMAGE_WIDTH))
            c = pygame.transform.scale(img, dim)
            clothes[i].append(c)
        except:
            pass
    
    return clothes
