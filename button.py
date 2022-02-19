import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self,button_width,button_height,center_x,center_y,button_text,button_color,text_color,text_font):
        super().__init__()

        self.image = pygame.Surface((button_width,button_height))
        self.image.fill(button_color)
        self.rect = self.image.get_rect(center=(center_x,center_y))
        text = text_font.render(button_text,True,text_color)
        self.image.blit(text,(button_width//2 - text.get_width()//2,button_height//2 - text.get_height()//2))


    def clicked_on(self,point):

        return self.rect.collidepoint(point)







