import pygame
from Constant import *
from Constant import Hanger
import math
'''
Available clothes display page
'''

class Closet:
    def __init__(self, win, clothes, font):
        self.win = win
        self.font = font
        self.page = 0
        self.rows = 1
        self.clothes = [] # list of Hangers
        self.pressing = False
        self.cur_key = None
        self.selected = [] # selected status
        self.displaying = [] # inds of displaying clothes

        self.clothes_out = [] # copy to be passed out (without modification)
        self.organizeClothes(clothes)
    
    def to_closet(self):
        self.get_page(self.page)

    def update(self, text, event):
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
            print(self.getSelected())


        for i in self.displaying:
            changed = 0
            for ev in event:
                changed = changed or self.clothes[i].on_click(ev)
            if self.selected[i] != self.clothes[i].selected or changed:
                print("changed:", changed)
                self.get_page(self.page)
            self.selected[i] = self.clothes[i].selected
            

        return to_home

    '''
    display saved outfits at given page
    '''
    def get_page(self, page):
        if len(self.clothes) <= page * self.rows * self.img_per_row or page < 0:
            return

        self.win.fill(MUTED_WHITE) # muted white
        total_page = math.ceil(len(self.clothes) / (self.rows * self.img_per_row))
        page_label = self.font.render("page " + str(page + 1)+"/" + str(total_page), 1, AQUA)
        self.win.blit(page_label, LABEL_LOC3)

        label = self.font.render("Closet", 1, MUTED_BLACK)
        self.win.blit(label, LABEL_LOC2)
        
        if page != 0:
            label_l = self.font.render("Back", 1, MATCHA)
            self.win.blit(label_l, (left_btn.pos[0] + 10, left_btn.pos[1] + 60))
            left_btn.show(win=self.win)
        if page != total_page - 1:
            label_r = self.font.render("Next", 1, MATCHA)
            self.win.blit(label_r, (right_btn.pos[0] - 40, right_btn.pos[1] + 60))
            right_btn.show(win=self.win)


        self.page = page
        self.displaying = []
        start_i = self.page * self.img_per_row * self.rows
        i = 0
        x = X
        y = Y
        while start_i + i < len(self.clothes) and i < self.rows * self.img_per_row:
            loc = (x, i // self.img_per_row * (DISPLAY_SIZE + DIST) + y)
            self.clothes[start_i + i].setPos(loc)
            self.displaying.append(start_i + i)
            self.clothes[start_i + i].show(self.win)
            # self.win.blit(self.clothes[start_i + i], loc)
            x += DISPLAY_SIZE + DIST
            i += 1
            if i == self.img_per_row:
                x = X

    '''
    Resize images of clothes and create Hanger instances for each clothes
    '''
    def organizeClothes(self, clothes):
        for i in range(len(clothes)):
            # w = self.clothes[i][0].get_width()
            # h = self.clothes[i][0].get_height()

            # # default width/height scale bounded by display_size
            # if h > w:
            #     ratio = DISPLAY_SIZE / h
            #     dim = (ratio * w, DISPLAY_SIZE)
            # else:
            #     ratio = DISPLAY_SIZE / w
            #     dim = (DISPLAY_SIZE, ratio * h)
            # self.clothes[i][0] = pygame.transform.scale(self.clothes[i][0], dim)
            
            # rescale the clothes images
            clothes[i] = [self.rescale(clothes[i][j]) for j in range(len(clothes[i]))]
            cur_c = Hanger((-1, -1), clothes[i], i)

            self.clothes.append(cur_c)

            # copy clothes to be passed out
            c_c = [c.copy() for c in clothes[i]]
            copy_c = Hanger((-1, -1), c_c, i)
            self.clothes_out.append(copy_c)

        # compute format for display
        self.img_per_row = (self.win.get_width() - X) // (DISPLAY_SIZE + DIST)
        # set selected status
        self.selected = [0]*len(self.clothes)


    '''
    Rescale a photo to be bounded by box with length = DISPLAY_SIZE
    img: image to be rescaled
    return img: rescaled image
    '''
    def rescale(self, img):
        w = img.get_width()
        h = img.get_height()

        # default width/height scale bounded by display_size
        if h > w:
            ratio = DISPLAY_SIZE / h
            dim = (ratio * w, DISPLAY_SIZE)
        else:
            ratio = DISPLAY_SIZE / w
            dim = (DISPLAY_SIZE, ratio * h)
        return pygame.transform.scale(img, dim)

    # return a list of selected clothes (Hanger obj)
    def getSelected(self):
        clothes = []
        for i in range(len(self.selected)):
            if self.selected[i]:
                clothes.append(self.clothes_out[i])
        return clothes

    def getNumSelected(self):
        return sum(self.selected)