import pygame
'''
Home page: screen showing the user and outfits
fitting onto them
'''

class Home:
    def __init__(self, num_clothes):
        self.person = False
        self.pressing = False
        self.cur_key = None
        self.clothes_i = 0
        self.num_clothes = num_clothes

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'c'
        elif keys[pygame.K_LEFT]:
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'left'
        elif self.pressing:
            self.pressing = False
            if self.cur_key == 'c':
                self.person = not self.person
                print('showing clothes:', self.person)
            elif self.cur_key == 'left' and self.person:
                self.clothes_i = (self.clothes_i+1) % self.num_clothes
                print('next clothes')
        
        return self.person, self.clothes_i