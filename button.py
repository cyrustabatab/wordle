import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self,button_width,button_height,center_x,center_y,button_text,button_color,text_color,text_font):
        super().__init__()

        self.image = pygame.Surface((button_width,button_height))
        self.button_color  = button_color
        self.image.fill(button_color)
        self.rect = self.image.get_rect(center=(center_x,center_y))
        self.text_font = text_font
        self.text_color = text_color
        text = text_font.render(button_text,True,text_color)
        self.original_text = text
        self.image.blit(text,(button_width//2 - text.get_width()//2,button_height//2 - text.get_height()//2))
    
    def set_text(self,text):
        text = self.text_font.render(text,True,self.text_color)
        self.image.fill(self.button_color)
        self.image.blit(text,(self.image.get_width()//2 - text.get_width()//2,self.image.get_height()//2 - text.get_height()//2))
    
    def set_original(self):
        self.image.fill(self.button_color)
        self.image.blit(self.original_text,(self.image.get_width()//2 - text.get_width()//2,self.image.get_height()//2 - text.get_height()//2))
    
    def get_bottom(self):
        return self.rect.bottom
    def clicked_on(self,point):

        return self.rect.collidepoint(point)







