import pygame
import sys
import os
from button import Button
from diffmenu import diffmenu
from solverScreen import solverScreen

pygame.init()
pygame.font.init()
pygame.mixer.init(22050, 16, 2, 512)
pygame.mixer.music.load(os.path.join('game_assets', 'bgmusic.mp3'))
pygame.mixer.music.play(-1, 500)
pygame.display.set_caption('Sudoku')
screen = pygame.display.set_mode((480, 480))
clock = pygame.time.Clock()

# image and font type
button_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','button.png')), (300, 80))
title_font = pygame.font.Font(os.path.join('game_assets', 'Boba.otf'), 60)
button_font = pygame.font.Font(os.path.join('game_assets', 'Boba.otf'), 30)

# button
game_btn = Button(button_img, 240 - button_img.get_width() // 2, 160, 40, 'Sudoku Game')
solver_btn = Button(button_img, 240 - button_img.get_width() // 2, 260, 40, 'Sudoku Solver')


# font
sudoku_font = title_font.render('Sudoku', True, (0, 0, 0))


# button_click bool
isDiffMenu = False
isSolver = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_btn.click(pos[0], pos[1]):
                isDiffMenu = True
                diffMenu = diffmenu()
                diffMenu.run()
                del diffMenu
                isDiffMenu = False
            if solver_btn.click(pos[0], pos[1]):
                screen = pygame.display.set_mode((720, 480))
                isSolver = True
                solver_screen = solverScreen()
                solver_screen.run()
                del solver_screen
                screen = pygame.display.set_mode((480, 480))
                isSolver = False




    # draw the screen
    screen.fill((153,255,255))
    screen.blit(screen, (0, 0))

    # draw title and button
    screen.blit(sudoku_font, (240 - sudoku_font.get_width() // 2, 60))
    game_btn.draw(screen)
    solver_btn.draw(screen)


    pygame.display.flip()
    clock.tick(10)
