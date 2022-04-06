import math
from Body import * 
from Constant import *


'''
calculate distance from locations
'''
def calc_dist(loc1, loc2):
    return math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)

'''
resize the given cloth based on distance
of user from the screen
'''

def fitClothes(cloth, location, cloth_type, margin = 0.8):
    w = cloth.get_width()
    h = cloth.get_height()
    
    # 10% of margin
    if cloth_type == ClothType.UPPER: # Check shoulder
        if not location[1] or not location[0]:
            return cloth
        shoulder_w =  calc_dist(location[1], location[0])
        dim_w = shoulder_w * (1 + margin) 
        dim_h = h / w * dim_w

    else: # Check hip
        if not location[3] or not location[2]:
            return cloth
        hip_w = calc_dist(location[3], location[2])
        dim_w = hip_w * (1 + margin) 
        dim_h = h / w * dim_w

    return pygame.transform.scale(cloth, (dim_w, dim_h))


'''
fit the cloth coordinate based on body tracking
'''
def fitCoords (location, cloth_type, margin_w = 0.35, margin_h = 0.25):
    offset = [40, 100]

    if cloth_type == ClothType.UPPER:
        if not location[1] or not location[0]:
            return offset
        shoulder_w = calc_dist(location[1], location[0])
        offset[0] = location[0][0] -shoulder_w * margin_w
        offset[1] =  location[0][1] - shoulder_w * margin_h
    else:
        if not location[2] or not location[3]:
            return offset
        hip_w = calc_dist(location[3], location[2])
        offset[0] = location[2][0] - shoulder_w * margin_w
        offset[1] = location[2][1] -shoulder_w * margin_h

    return max(offset[0], 0), max(offset[1], 0)