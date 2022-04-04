import numpy as np
import pygame

'''
pixel: a tuple of (R, G, B)

return: a 2-d tuple of (luminance, (kr,kg,kb))
'''
def lumiChromi(pixel):
    s_lumi = sum(pixel)
    lumi = sum(pixel) // 3
    if s_lumi == 0:
        s_lumi = 1
    chromi = (pixel[0]//s_lumi, pixel[1]//s_lumi, pixel[2]//s_lumi)
    return lumi, chromi

'''
cloth: an surface object of a cloth
new_color: an RGB color filter 

return: a surface with changed color
'''
def change_color(cloth, new_color):
    _, new_chromi = lumiChromi(new_color)
    width = cloth.get_width()
    height = cloth.get_height()
    ret_surface = cloth.copy()
    for w in range(width):
        for h in range(height):
            r, g, b, a = cloth.get_at((w, h))
            if a != 0:
                lumi, _ = lumiChromi((r,g,b))
                new_pix = (lumi * new_chromi[0], lumi * new_chromi[1], lumi * new_chromi[2], a)
                ret_surface.set_at((w, h), new_pix)
    return ret_surface

'''
image: the video image for spotting the lightest point
cloth: an image object of a cloth
new_color: an RGB color filter 

return: a surface with changed color
'''
def rescale_light(image, cloth, new_cloth):
    pass