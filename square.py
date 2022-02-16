import pygame
from colors import *




class Square(pygame.sprite.Sprite):

    
    SELECT_COLOR = (0,0,0,150)
    SQUARE_COLOR = (255,255,255)
    FONT = pygame.font.SysFont("calibri",40)
    def __init__(self,topleft_x,topleft_y,width,height):
        super().__init__()


        self.image = pygame.Surface((width,height))
        self.color = self.SQUARE_COLOR
        self.image.fill(self.color)

        self.trans_rect = pygame.Surface((width,height),flags=pygame.SRCALPHA)
        self.trans_rect.fill(self.SELECT_COLOR)
        self.text = None



        self.current_selection = False
        self.rect = self.image.get_rect(topleft=(topleft_x,topleft_y))
        self.has_text = False


    def draw(self,screen):
        screen.blit(self.image,self.rect)
        if self.current_selection:
            screen.blit(self.trans_rect,self.rect)


    
    def set_text(self,text):

        text  = self.FONT.render(text,True,(0,) * 3)
        self.text = text
        self.image.fill(self.SQUARE_COLOR)
        self.image.blit(text,(self.image.get_width()//2 - text.get_width()//2,self.image.get_height()//2 - text.get_height()//2))
        self.text = text


    def delete(self):
        
        if self.text:
            self.text = None
            self.image.fill(self.SQUARE_COLOR)

    def set_current_selection(self):
        self.current_selection = True
            

    def unset_selection(self):
        self.current_selection = False


