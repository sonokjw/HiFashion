import pygame
'''
Favorite Outfits (screenshots) display page
'''

OUTFIT_WIDTH = 350
LABEL_LOC = (450, 50)
MUTED_WHITE = (249, 245, 236)
MUTED_BLACK = (18,18,18)

class Fav:
    def __init__(self, win, font):
        self.win = win
        self.font = font
        self.page = 0
        self.rows = 2
        self.height = 250
        self.outfits = []
        self.pressing = False
        self.cur_key = None

        self.compute_format()
    
    def to_fav(self):
        self.get_page(self.page)

    '''
    Detection of commands of going to different pages
    '''
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
    Initialization of previous saved outfits and class variables
    '''
    def compute_format(self):
        w, h = self.win.get_width(), self.win.get_height()
        # Load Saved Outfits
        j = 0
        while True:
            try:
                img = pygame.image.load(f'favs/{j}.png')
                dim = (OUTFIT_WIDTH, int(float(img.get_height())/img.get_width()*OUTFIT_WIDTH))
                c = pygame.transform.scale(img, dim)
                self.outfits.append(c)
            except:
                break
            j += 1
        
        self.img_per_row = (w - 50) // (OUTFIT_WIDTH + 25)
        if j > 0:
            self.height = self.outfits[0].get_height()

    '''
    display saved outfits at given page
    '''
    def get_page(self, page):
        if len(self.outfits) <= page * self.rows * self.img_per_row or page < 0:
            return
        
        self.win.fill(MUTED_WHITE) # muted white
        label = self.font.render("Saved Outfits", 1, MUTED_BLACK)
        self.win.blit(label, LABEL_LOC)
        
        self.page = page

        start_i = self.page * self.img_per_row * self.rows
        i = 0
        x = 50
        y = 150
        while start_i + i < len(self.outfits) and i < self.rows * self.img_per_row:
            loc = (x, i // self.img_per_row * (self.height + 25) + y)
            self.win.blit(self.outfits[start_i + i], loc)
            x += self.outfits[start_i + i].get_width() + 25
            i += 1
            if i == self.img_per_row:
                x = 50

    '''
    Save the current screenshot to saved outfits, located in /favs
    in files, and add it to Saved Outfit page
    img: screenshot to be saved
    '''
    def saveOutfit(self, img):
        pygame.image.save(img, f'favs/{len(self.outfits)}.png')
        # img = pygame.image.load(f'favs/{len(self.outfits)-1}.png')
        dim = (OUTFIT_WIDTH, int(float(img.get_height())/img.get_width()*OUTFIT_WIDTH))
        img = pygame.transform.scale(img, dim)
        self.outfits.append(img)
        if len(self.outfits) == 1:
            self.height = self.outfits[0].get_height()
        print("Outfit Saved!")