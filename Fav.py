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

        self.compute_format()
    
    def to_fav(self):
        self.win.fill(MUTED_WHITE) # muted white
        label = self.font.render("Saved Outfits", 1, MUTED_BLACK)
        self.win.blit(label, LABEL_LOC)
        
        start_i = self.page * self.img_per_row
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


    def update(self):
        pass
        
    
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
    Save the current screenshot to saved outfits, located in /favs
    in files, and add it to Saved Outfit page
    img: screenshot to be saved
    '''
    def saveOutfit(self, img):
        pygame.image.save(img, f'favs/{len(self.outfits)}.png')
        dim = (OUTFIT_WIDTH, int(float(img.get_height())/img.get_width()*OUTFIT_WIDTH))
        img = pygame.transform.scale(img, dim)
        self.outfits.append(img)
        print("Outfit Saved!")