import pygame,sys
pygame.init()

from colors import *
from square import Square
from collections import Counter
from button import Button
import random




class Game:
    
    SCREEN_HEIGHT = 700
    BGCOLOR = (128,128,128)
    SCREEN_WIDTH = 600
    SQUARE_SIZE = 75
    BOTTOM_SECTION_HEIGHT= 150
    GAP = 10
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50
    FPS = 30
    TEXT_DISPLAY_TIME = 1000
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
        self.word_to_guess = 'ZIICC'
        print(self.word_to_guess)
        self._create_text()
        self.show_text = False
        self.text = None
        self.game_over = False

        self.current_row =self.current_col =  0
        self.word_typed = [None] * 5
    
    def _create_text(self):
        

        texts = ('TRY AGAIN',"MISSING LETTERS","INVALID WORD",f"WORD WAS {self.word_to_guess.upper()}") 
        
        self.text_renders  = {}
        for text in texts:
            text_image = self.FONT.render(text,True,RED)
            text_rect = text_image.get_rect(center=(self.screen_width//2,self.submit_button.sprite.get_bottom() + self.GAP + text_image.get_height()//2))
            self.text_renders[text] = (text_image,text_rect)
        self.TEXT_EVENT = pygame.USEREVENT + 2
    
    def _reset(self):
        for square in self.squares:
            square.delete()
        self.submit_button.sprite.set_original()
        self.game_over = False
        self.text = None
        self.word_typed = [None] * self.word_length

        self._choose_random_word()
        self._create_text()
        self.current_row =self.current_col =  0
        self._switch_selection()
    def _choose_random_word(self):

        self.word_to_guess = random.choice(self.words)
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
        if self.text:
            self.screen.blit(self.text,self.text_rect)

    

    def _switch_selection(self,unset=True):
        self.current_selection.unset_selection()
        self.current_selection = self.board[self.current_row][self.current_col]
        self.current_selection.set_current_selection()
    
    def _check_correctness(self,word):

        

        counts_letters = Counter(self.word_to_guess)

        for i,(guessed_letter,true_letter) in enumerate(zip(word,self.word_to_guess)):
            if guessed_letter == true_letter:
                self.board[self.current_row][i].set_color(GREEN)
                counts_letters[true_letter] -= 1
            elif guessed_letter not in self.word_to_guess:
                self.board[self.current_row][i].set_color(LIGHT_RED)
            elif guessed_letter in self.word_to_guess:
                if counts_letters[guessed_letter] != 0:
                    self.board[self.current_row][i].set_color(YELLOW)
                    counts_letters[guessed_letter] -= 1
                else:
                    self.board[self.current_row][i].set_color(LIGHT_RED)

        
        



        



    def _check_word_typed(self):

        # check which letters are correct if any and change the background color of each square
        self.show_text = True
        skip = False
        if not all(value for value in self.word_typed):
            text_type = 'MISSING LETTERS'
        else:
            word = ''.join(self.word_typed)

            if word in self.words:


                self._check_correctness(word)

                if word == self.word_to_guess:
                    print('correct')
                    self.game_over = True
                else:
                    print('incorrect')
                    if self.current_row + 1 ==self.guesses:

                        text_type = f'WORD WAS {self.word_to_guess.upper()}'
                        self.game_over = True
                        skip = True
                
                if self.game_over:
                    self.current_selection.unset_selection()

                
                if not skip:
                    self.current_row = self.current_row + 1
                    self.word_typed = [None] * 5
                    self.current_col = 0
                    self._switch_selection(unset=False)
                    text_type = 'TRY AGAIN'
            else:
                text_type = 'INVALID WORD'
            
        self.text,self.text_rect = self.text_renders[text_type]
        if not skip:
            pygame.time.set_timer(self.TEXT_EVENT,self.TEXT_DISPLAY_TIME,1)
    

    def play(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.text and event.type == self.TEXT_EVENT:
                    self.text = None
                elif event.type == pygame.KEYDOWN:
                    arrow = backspace = False
                    
                    if not self.game_over:
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
                            print(self.word_typed)
                            self._check_word_typed()
                            if self.game_over:
                                self.submit_button.sprite.set_text("PLAY AGAIN")
                    elif event.key == pygame.K_RETURN:
                        self._reset()





                    if arrow:
                        self.current_selection.unset_selection()
                        if not (backspace and self.current_col == 0):
                            self.current_col = (self.current_col + direction) % self.word_length
                        self.current_selection = self.board[self.current_row][self.current_col]
                        self.current_selection.set_current_selection()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    point = pygame.mouse.get_pos()
                    if not self.game_over:
                        if self.submit_button.sprite.clicked_on(point):
                            self._check_word_typed()
                            if self.game_over:
                                self.submit_button.sprite.set_text("PLAY AGAIN")

                    else:
                        if self.submit_button.sprite.clicked_on(point):
                            self.submit_button.sprite.set_text("SUBMIT")
                            self._reset()

                    

            
            self._draw()
            pygame.display.update()
            self.clock.tick(self.FPS)



