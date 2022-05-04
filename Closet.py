import pygame
from Constant import Hanger
'''
Available clothes display page
'''

DISPLAY_SIZE = 250
LABEL_LOC = (480, 50)
MUTED_WHITE = (249, 245, 236)
MUTED_BLACK = (18,18,18)

class Closet:
    def __init__(self, win, clothes, font):
        self.win = win
        self.font = font
        self.page = 0
        self.rows = 1
        self.clothes = []
        self.pressing = False
        self.cur_key = None

        self.clothes_dict = {} # ind of cloth to hanger
        self.selected = [] # inds of selected clothes

        self.organizeClothes(clothes)
    
    def to_closet(self):
        self.get_page(self.page)

    def update(self, text):
        to_home = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: # next page
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'right'
        elif keys[pygame.K_LEFT]: # next page
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'left'
        elif self.pressing: # key relased
            self.pressing = False
            if self.cur_key == 'right':
                self.get_page(self.page + 1)
                print('next page')
            elif self.cur_key == 'left':
                self.get_page(self.page - 1)
                print('previous page')

        txt_ls = text.split(" ")
        if "back" in txt_ls:
            self.get_page(self.page - 1)
        elif 'next' in txt_ls:
            self.get_page(self.page + 1)
        elif 'home' in txt_ls or 'homepage' in txt_ls:
            to_home = True
        
        return to_home

    '''
    display saved outfits at given page
    '''
    def get_page(self, page):
        if (len(self.clothes)) <= page * self.rows * self.img_per_row or page < 0:
            return
        
        self.win.fill(MUTED_WHITE) # muted white
        label = self.font.render("Saved Outfits", 1, MUTED_BLACK)
        self.win.blit(label, LABEL_LOC)
        
        self.page = page

        start_i = self.page * self.img_per_row * self.rows
        i = 0
        x = 50
        y = 150
        while start_i + i < len(self.clothes) and i < self.rows * self.img_per_row:
            loc = (x, i // self.img_per_row * (DISPLAY_SIZE + 25) + y)
            self.win.blit(self.clothes[start_i + i], loc)
            x += self.clothes[start_i + i].get_width() + 25
            i += 1
            if i == self.img_per_row:
                x = 50


    def organizeClothes(self, clothes):
        self.clothes = [c for c in clothes]
        for i in range(len(self.clothes)):
            w = self.clothes[i].get_width()
            h = self.clothes[i].get_height()

            # default width/height scale bounded by display_size
            if h > w:
                ratio = DISPLAY_SIZE / h
                dim = (ratio * w, DISPLAY_SIZE)
            else:
                ratio = DISPLAY_SIZE / w
                dim = (DISPLAY_SIZE, ratio * h)
            self.clothes[i] = pygame.transform.scale(self.clothes[i], dim)

        # compute format for display
        self.img_per_row = (self.win.get_width() - 50) // (DISPLAY_SIZE + 25)


    