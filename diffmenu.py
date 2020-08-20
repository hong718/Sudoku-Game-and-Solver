import pygame
import sys
import os
from button import Button
from gameScreen import gameScreen

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((480, 480))
clock = pygame.time.Clock()

# image and font type
button_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','button.png')), (300, 80))
title_font = pygame.font.Font(os.path.join('game_assets', 'Boba.otf'), 60)
button_font = pygame.font.Font(os.path.join('game_assets', 'Boba.otf'), 30)

# button

back_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','back.png')), (60, 60))

# font
sudoku_font = title_font.render('Sudoku', True, (0, 0, 0))




class diffmenu():
    def __init__ (self):
        self.screen = screen
        self.isRun = True
        self.back_btn = Button(back_img, 410, 20)
        self.easy_btn = Button(button_img, 240 - button_img.get_width() // 2, 160, 40, 'Easy')
        self.medium_btn = Button(button_img, 240 - button_img.get_width() // 2, 260, 40, 'Medium')
        self.difficult_btn = Button(button_img, 240 - button_img.get_width() // 2, 360, 40, 'Difficult')

    def run(self):
        while self.isRun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # check which difficulty is chosen
                    if self.easy_btn.click(pos[0], pos[1]):
                        self.screen = pygame.display.set_mode((720, 480))
                        g = gameScreen('easy')
                        g.run()
                        self.screen = pygame.display.set_mode((480, 480))
                        self.isRun = False
                    if self.medium_btn.click(pos[0], pos[1]):
                        self.screen = pygame.display.set_mode((720, 480))
                        g = gameScreen('medium')
                        g.run()
                        self.screen = pygame.display.set_mode((480, 480))
                        self.isRun = False
                    if self.difficult_btn.click(pos[0], pos[1]):
                        self.screen = pygame.display.set_mode((720, 480))
                        g = gameScreen('difficult')
                        g.run()
                        self.screen = pygame.display.set_mode((480, 480))
                        self.isRun = False

                    # check whether the back button is clicked
                    if self.back_btn.click(pos[0], pos[1]):
                        self.isRun = False


            # draw the screen
            self.screen.fill((153,255,255))
            self.screen.blit(screen, (0, 0))

            # draw title and button
            self.screen.blit(sudoku_font, (240 - sudoku_font.get_width() // 2, 60))
            self.easy_btn.draw(screen)
            self.medium_btn.draw(screen)
            self.difficult_btn.draw(screen)
            self.back_btn.draw(screen)

            pygame.display.flip()
            clock.tick(10)
