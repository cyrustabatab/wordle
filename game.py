import pygame,sys
pygame.init()

from colors import *
from square import Square
from button import Button
import random




class Game:
    
    SCREEN_HEIGHT = 600
    BGCOLOR = (128,128,128)
    SCREEN_WIDTH = 600
    SQUARE_SIZE = 75
    BOTTOM_SECTION_HEIGHT= 100
    GAP = 10
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50
    FPS = 30
    WORDS_FILE = "words.txt"
    FONT = pygame.font.SysFont("calibri",40)


    def __init__(self,guesses=6,word_length=5):

        self.guesses = guesses
        self.word_length = word_length
        self.screen_height = self.GAP + (self.guesses) * (self.SQUARE_SIZE + self.GAP) + self.BOTTOM_SECTION_HEIGHT
        self.screen_width = self.GAP + (self.word_length) * (self.SQUARE_SIZE + self.GAP)
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.clock = pygame.time.Clock()
        self._create_buttons()
        self._create_board()
        self._load_words()
        self._choose_random_word()
        self.current_row =self.current_col =  0
        self.word_typed = [None] * 5
    

    def _choose_random_word(self):

        self.word_to_guess = random.choice(self.words)
        print(self.word_to_guess)
    def _create_buttons(self): 

        submit_button = Button(self.BUTTON_WIDTH,self.BUTTON_HEIGHT,self.screen_width//2,self.GAP + (self.SQUARE_SIZE + self.GAP) * self.guesses + 50,"SUBMIT",RED,BLACK,self.FONT)
        self.submit_button = pygame.sprite.GroupSingle(submit_button)

    def _load_words(self):

        with open(self.WORDS_FILE,'r') as f:
            self.words = list(map(lambda s: s.strip().upper(),f.readlines()))


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

        self.submit_button.draw(self.screen)
    

    def _switch_selection(self):
        self.current_selection.unset_selection()
        self.current_selection = self.board[self.current_row][self.current_col]
        self.current_selection.set_current_selection()
    
    def _check_word_typed(self):


        word = ''.join(self.word_typed)

        if word in self.words:

            if word == self.word_to_guess:
                print('correct')
            else:
                print('incorrect')


            self.current_row = self.current_row + 1
            self.current_col = 0
            self._switch_selection()
        else:
            print('not a valid word')

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
                        self.word_typed[self.current_col] = key
                        self.current_col = min(self.word_length - 1,self.current_col + 1)
                        self.current_selection.unset_selection()
                        self.current_selection = self.board[self.current_row][self.current_col]
                        self.current_selection.set_current_selection()
                    elif event.key == pygame.K_BACKSPACE:
                        self.current_selection.delete()
                        self.word_typed[self.current_col] = None
                        arrow = True
                        direction = -1
                        backspace = True
                    elif event.key == pygame.K_RETURN:
                        if all(value for value in self.word_typed):
                            self._check_word_typed()
                        else:
                            print('please type out all letters')





                    if arrow:
                        self.current_selection.unset_selection()
                        if not (backspace and self.current_col == 0):
                            self.current_col = (self.current_col + direction) % self.word_length
                        self.current_selection = self.board[self.current_row][self.current_col]
                        self.current_selection.set_current_selection()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    if self.submit_button.sprite.clicked_on(point):
                        if all(value for value in self.word_typed):
                            self._check_word_typed()
                        else:
                            print('please type out all letters')


                    

            
            self._draw()
            pygame.display.update()
            self.clock.tick(self.FPS)



