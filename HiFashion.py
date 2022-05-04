import pygame
import pygame.camera
import pygame.image
import pygame.mixer
import time
import sys

from FitClothes import fitClothes, fitCoords
from Constant import *
from ChangeColor import *

from Home import Home
from Fav import Fav
from Closet import Closet
from Body import Body
from Speech import Speech

from threading import Thread
import threading


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

new_clothes = {} # a dictionary saving new clothing colors based on color scheme

# in case we want another number of clothes
if len(sys.argv) > 1:
    NUM_CLOTHES = min(NUM_CLOTHES, int(sys.argv[1]))

# App Display Setup
pygame.init()
pygame.camera.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("HiFashion")

# Webcam Setup
user_cam = pygame.camera.list_cameras()[0]
cam = pygame.camera.Camera(user_cam, (CAM_WIDTH, CAM_HEIGHT))
cam.start()
cam.set_controls(hflip = True, vflip = False)

# Text Setup
font = pygame.font.SysFont("helvetica", 48)
screenshot_font = pygame.font.SysFont("helvetica", 125)

# Audio Setup
pygame.mixer.init()
pygame.mixer.music.load("screenshot.wav")
pygame.mixer.music.set_volume(0.7)

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

# Tracking tools setup
body = Body(WIN_WIDTH, WIN_HEIGHT)
speech = Speech()
cur_time = pygame.time.get_ticks()

########### App Loop ###########
while not ended:
    # buttons or quit events
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            ended = True
        if cur_mode != Modes.FAV:
            new_mode, change = closet_btn.on_click(event, cur_mode)
            if new_mode is not None:
                cur_mode = new_mode
                if change:
                    closet_pg.to_closet()
        if cur_mode != Modes.CLOSET:
            new_mode, change = fav_btn.on_click(event, cur_mode)
            if new_mode is not None:
                cur_mode = new_mode
                if change:
                    fav_pg.to_fav()

    # speech detection
    if threading.active_count() <= 1:
        Thread(target=speech.get_text, args=()).start()

    # update current page
    if cur_mode == Modes.HOME:
        image = cam.get_image()
        win.blit(image, (0,0))
        person, clothes_i, color_i, screenshot, tracking, fit, page = home_pg.update(speech.text)

        if person:
            if fit:
                body.track(image)
            cloth = clothes[clothes_i]
            # change color
            ind = color_i % (len(MORANDI) + 1)
            if clothes_i not in new_clothes:
                new_clothes[clothes_i] = [cloth]
                for color in MORANDI:
                    new_clothes[clothes_i].append(change_color(cloth, color))
            cloth = new_clothes[clothes_i][ind]
            cloth = fitClothes(cloth, body.locations, cloth_dic[clothes_i]['ctype'], cloth_dic[clothes_i]['margin'])
            coord = fitCoords(body.locations, cloth_dic[clothes_i]['ctype'], cloth_dic[clothes_i]['margin_w'], cloth_dic[clothes_i]['margin_h'])
            # print("clothes at coord: ", coord)
            win.blit(cloth, coord)
        # taking a screenshot
        if screenshot:
            fav_pg.saveOutfit(win)
            pygame.mixer.music.play()
            label = screenshot_font.render("OUTFIT SAVED!", 1, MUTED_WHITE)
            win.blit(label, (100, 200))
            pygame.display.update()
            time.sleep(1.5)
        # showing tracking skeletons of shoulder and hip
        if tracking:
            body.draw(win)
        # new page by voice commands
        if page == Modes.CLOSET:
            cur_mode = Modes.CLOSET
            closet_pg.to_closet()
        elif page == Modes.FAV:
            cur_mode = Modes.FAV
            fav_pg.to_fav()
    elif cur_mode == Modes.CLOSET:
        to_home = closet_pg.update(speech.text)
        if to_home:
            cur_mode = Modes.HOME
    else: # Fav
        to_home = fav_pg.update(speech.text)
        if to_home:
            cur_mode = Modes.HOME

    # update button display
    if cur_mode != Modes.FAV:
        closet_btn.show(win=win)
    if cur_mode != Modes.CLOSET:
        fav_btn.show(win=win)
    
    pygame.display.update()
        
pygame.quit()