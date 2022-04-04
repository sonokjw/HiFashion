import pygame
'''
Available clothes display page
'''

DISPLAY_SIZE = (100, 100)
LABEL_LOC = (480, 50)
MUTED_WHITE = (249, 245, 236)
MUTED_BLACK = (18,18,18)

class Closet:
    def __init__(self, win, clothes, font):
        self.win = win
        self.font = font
        self.organizeClothes(clothes)
    
    def to_closet(self):
        self.win.fill(MUTED_WHITE)
        label = self.font.render("My Closet", 1, MUTED_BLACK)
        self.win.blit(label, LABEL_LOC)

    def update(self):
        pass

    def organizeClothes(self, clothes):
        self.clothes = [c for c in clothes]
        for i in range(len(self.clothes)):
            pygame.transform.scale(self.clothes[i], DISPLAY_SIZE)
    