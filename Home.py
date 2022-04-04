import pygame
'''
Home page: screen showing the user and outfits
fitting onto them
'''

class Home:
    def __init__(self, num_clothes):
        self.person = False
        self.pressing = False
        self.color = 0
        self.cur_key = None
        self.clothes_i = 0 # i of clothes being displayed
        self.num_clothes = num_clothes

    # detect key press
    def update(self):
        screenshot = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]: # show clothes
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'c'
        elif keys[pygame.K_LEFT]: # next clothes
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'left'
        elif keys[pygame.K_UP]: # next color
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'up'
        elif keys[pygame.K_p]: # screenshot
            if not self.pressing:
                self.pressing = True
                self.cur_key = 'p'
        elif self.pressing: # key relased
            self.pressing = False
            if self.cur_key == 'c':
                self.person = not self.person
                print('showing clothes:', self.person)
            elif self.cur_key == 'left' and self.person:
                self.clothes_i = (self.clothes_i+1) % self.num_clothes
                self.color = 0
                print('next clothes')
            elif self.cur_key == 'up' and self.person:
                self.color += 1
                print('next color')
            elif self.cur_key == 'p':
                screenshot = True
        
        return self.person, self.clothes_i, screenshot

'''
Save the current screenshot to saved outfits, located in /favs
in files
img screenshot to be saved
num outfit number
'''
def saveOutfit(img, num):
    pygame.image.save(img, f'favs/{num}.png')
    print("Outfit Saved!")