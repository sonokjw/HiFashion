'''
Favorite Outfits (screenshots) display page
'''

DISPLAY_SIZE = (100, 100)
LABEL_LOC = (450, 50)
MUTED_WHITE = (249, 245, 236)
MUTED_BLACK = (18,18,18)

class Fav:
    def __init__(self, win, outfits, font):
        self.win = win
        self.outfits = outfits
        self.font = font
        self.compute_format()
    
    def to_fav(self):
        self.win.fill(MUTED_WHITE) # muted white
        label = self.font.render("Saved Outfits", 1, MUTED_BLACK)
        self.win.blit(label, LABEL_LOC)
        

    def update(self):
        pass
        
    
    def compute_format(self):
        w, h = self.win.get_width(), self.win.get_height()