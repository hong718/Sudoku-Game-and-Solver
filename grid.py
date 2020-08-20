import pygame
import os

pygame.font.init()
text_font = pygame.font.Font(os.path.join('game_assets','Boba.otf'), 20)



class Grid():
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num
        self.width = 42


    def click(self, X ,Y):
        '''
        check whether a grid is clicked
        :param X: int
        :param Y: int
        :return: bool
        '''
        if X >= 30 + self.width * self.y and X <= 30 + self.width * (self.y + 1):
            if Y >= 60 + self.width * self.x and Y <= 60 + self.width * (self.x + 1):
               return True
        return False

    def draw(self, win, colour):
        '''
        draw the number in a grid
        :param win: surface
        :param colour: tuple(int)
        :return: None
        '''
        text = text_font.render(str(self.num), True, colour)
        win.blit(text, (30 + self.width * self.y + self.width // 2 - text.get_width() // 2, 60 + self.width * self.x + self.width // 2 - text.get_height() // 2))

    def drawRect(self, win, x, y):
        '''
        draw a rect around a grid when a grid is clicked
        :param win: surface
        :param x: int
        :param y: int
        :return: None
        '''
        pygame.draw.rect(win, (255, 0, 0), (30 + self.width * y, 60 + self.width * x, self.width, self.width), 2)
