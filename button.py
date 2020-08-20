import pygame
import os

pygame.font.init()

button_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','button.png')), (200, 60))


class Button():
    def __init__(self, img, x, y, text_size = 0, text = None):
        self.img = img
        self.text = text
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.text_font = pygame.font.Font(os.path.join('game_assets','Boba.otf'), text_size)

    def draw(self, win):
        '''
        draw the button on the screen
        :param win: surface
        :return: none
        '''
        win.blit(self.img, (self.x, self.y))
        if self.text is not None:
            text_input = pygame.font.Font.render(self.text_font, self.text, True, (0, 0, 0))
            win.blit(text_input, (self.x + self.img.get_width() // 2 - text_input.get_width() // 2, self.y + self.img.get_height() // 2 - text_input.get_height() // 2 ))

    def click(self, X, Y):
        '''
        check whether a button is clicked
        :param X: int
        :param Y: int
        :return: None
        '''
        if X <= self.x + self.img.get_width() and X >= self.x:
            if Y <= self.y + self.img.get_height() and Y >= self.y:
                return True
