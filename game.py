import pygame,sys
pygame.init()

from colors import *
from square import Square




class Game:
    
    SCREEN_HEIGHT = 600
    BGCOLOR = (128,128,128)
    SCREEN_WIDTH = 600
    SQUARE_SIZE = 75
    BOTTOM_SECTION_HEIGHT= 100
    GAP = 10
    FPS = 30


    def __init__(self,guesses=6,word_length=5):

        self.guesses = guesses
        self.word_length = word_length
        self.screen_height = self.GAP + (self.guesses) * (self.SQUARE_SIZE + self.GAP) + self.BOTTOM_SECTION_HEIGHT
        self.screen_width = self.GAP + (self.word_length) * (self.SQUARE_SIZE + self.GAP)
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.clock = pygame.time.Clock()
        self._create_board()
        self.current_row =self.current_col =  0




    def _create_board(self):

        
        self.squares = pygame.sprite.Group()
        self.board = []
        for row in range(self.guesses):
            board_row = []
            for col in range(self.word_length):
                x = self.GAP + ((self.SQUARE_SIZE + self.GAP) * col)
                y = self.GAP + ((self.SQUARE_SIZE + self.GAP) * row)
                square = Square(x,y,self.SQUARE_SIZE,self.SQUARE_SIZE)
                self.squares.add(square)
                board_row.append(square)
                if row == 0 and col == 0:
                    square.set_current_selection()
                    self.current_selection = square

            self.board.append(board_row)

        

    
    def _draw(self):
        self.screen.fill(self.BGCOLOR)
        for square in self.squares:
            square.draw(self.screen)


    


    def play(self):


        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    arrow = backspace = False

                    if event.key == pygame.K_RIGHT:
                        direction= 1
                        arrow = True
                    elif event.key == pygame.K_LEFT:
                        direction = -1
                        arrow = True
                    elif pygame.K_a <= event.key <= pygame.K_z:
                        key = chr(event.key).upper()
                        self.current_selection.set_text(key)
                        self.current_col = min(self.word_length - 1,self.current_col + 1)
                        self.current_selection.unset_selection()
                        self.current_selection = self.board[self.current_row][self.current_col]
                        self.current_selection.set_current_selection()
                    elif event.key == pygame.K_BACKSPACE:
                        self.current_selection.delete()
                        arrow = True
                        direction = -1
                        backspace = True





                    if arrow:
                        self.current_selection.unset_selection()
                        if not (backspace and self.current_col == 0):
                            self.current_col = (self.current_col + direction) % self.word_length
                        self.current_selection = self.board[self.current_row][self.current_col]
                        self.current_selection.set_current_selection()
                    

            
            self._draw()
            pygame.display.update()
            self.clock.tick(self.FPS)



