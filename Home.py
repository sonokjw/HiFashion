from operator import mod
import pygame
from Constant import *
import time
'''
Home page: screen showing the user and outfits
fitting onto them
'''

class Home:
    def __init__(self, num_clothes):
        self.person = False # fit clothes to user
        self.pressing = False
        self.color = 0
        self.cur_key = None
        self.clothes_i = 0 # i of selected clothes being displayed
        self.num_clothes = num_clothes
        self.tracking = False
        self.isBack = 0 # whether it's displaying the back of the current clothes

    '''
    Detect key press and voice commands.
    text: transcription of what the user says
    '''
    def update(self, text):
        fit = False
        page = Modes.HOME
        screenshot = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]: # show clothes
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'c'
        if keys[pygame.K_f]: # fit clothes to user once
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'f'
        elif keys[pygame.K_LEFT]: # next clothes
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'left'
        elif keys[pygame.K_UP]: # next color
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'up'
        elif keys[pygame.K_p]: # take a picture
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'p'
        elif keys[pygame.K_t]: # show tracking segments
            if not self.pressing:
                self.pressing = True
                self.cur_key = 't'
        elif self.pressing: # key relased
            self.pressing = False
            if self.cur_key == 'c':
                self.person = not self.person
                print('showing clothes:', self.person)
            elif self.cur_key == 'f' and self.person:
                fit = True
            elif self.cur_key == 'left' and self.person:
                self.clothes_i = (self.clothes_i+1) % self.num_clothes
                self.color = 0
                print('next clothes')
            elif self.cur_key == 'up' and self.person:
                self.color += 1
                print('next color')
            elif self.cur_key == 'p':
                screenshot = True
            elif self.cur_key == 't':
                self.tracking = not self.tracking
        
        # voice commands detection
        if 'my outfits' in text or 'my outfit' in text:
            page = Modes.FAV
            self.isBack = 0
        elif 'fit' in text:
            fit = True
            self.person = True
        elif 'clear' in text:
            self.person = False
        elif 'next' in text and self.person:
            self.clothes_i = (self.clothes_i+1) % self.num_clothes
            self.color = 0
            self.isBack = 0
            fit = True
        elif 'back' in text and self.person:
            self.clothes_i = (self.clothes_i-1) % self.num_clothes
            self.color = 0
            self.isBack = 0
            time.sleep(0.5)
        elif 'change color' in text and self.person:
            self.color += 1
            time.sleep(0.5)
        elif 'picture' in text:
            screenshot = True
        elif 'closet' in text:
            page = Modes.CLOSET
            self.isBack = 0
        elif 'turn' in text:
            self.isBack = 1 if self.isBack == 0 else 0
            time.sleep(0.5)
        
        return self.person, self.clothes_i, self.color, screenshot, self.tracking, fit, page

    def setNumClothes(self, num):
        self.num_clothes = num


    def getSide(self):
        return self.isBack