import pygame
from game import Game


if __name__ == "__main__":

    pygame.display.set_caption("WORDLE")
    game = Game()
    game.play()
