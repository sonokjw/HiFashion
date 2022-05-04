import enum
import csv

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

print(cloth_dic)
        