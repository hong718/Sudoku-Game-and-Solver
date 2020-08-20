import pygame
import sys
import os
from sudoku import Sudoku
from button import Button

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()


# button_img
large_button_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','button.png')), (200, 60))
back_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','back.png')), (60, 60))
sound_on_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','sound_on.png')), (60, 60))
sound_off_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','sound_off.png')), (60, 60))

# font
text_font = pygame.font.Font(os.path.join('game_assets','Boba.otf'), 40)
noSol_text = text_font.render('It has no solution!', True, (0, 0, 0))
hasSol_text = text_font.render('It has a solution!', True, (0, 0, 0))

# emptyBoard
empty = []
for i in range(9):
    for j in range(9):
        empty.append([0] * 9)


class solverScreen():
    def __init__(self):
        self.sudoku = Sudoku(30, 60)
        self.sudoku.genEmpty()
        self.isRun = True
        self.solve_btn = Button(large_button_img, 480, 170, 30, 'Solve')
        self.reset_btn = Button(large_button_img, 480, 250, 30, 'Reset')
        self.back_btn = Button(back_img, 650, 20)
        self.sound_on_btn = Button(sound_on_img, 580, 20)
        self.sound_off_btn = Button(sound_off_img, 580, 20)
        self.isMusic = True
        self.isGridSelected = False
        self.gridSelected = None
        self.question = empty
        self.hasSolution = True
        self.isSolve = False
        self.showResult = False

    def run(self):
        while self.isRun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.showResult = False
                    # check whether the music button is clicked
                    if self.isMusic and self.sound_on_btn.click(pos[0], pos[1]):
                        pygame.mixer.music.pause()
                        self.isMusic = False
                    elif not self.isMusic and self.sound_off_btn.click(pos[0], pos[1]):
                        pygame.mixer.music.unpause()
                        self.isMusic = True

                    # check whether the solve button is clicked
                    if self.solve_btn.click(pos[0], pos[1]):
                        self.isSolve = True

                    # check whether the back button is clicked
                    if self.back_btn.click(pos[0], pos[1]):
                        self.isRun = False

                    # check whether the reset button is clicked
                    if self.reset_btn.click(pos[0], pos[1]):
                        for i in range(9):
                            for j in range(9):
                                self.question[i][j] = 0
                                self.sudoku.grid_dict[(i, j)].num = 0

                    # check whether the grid is clicked
                    for key1, key2 in self.sudoku.grid_dict:
                        key = (key1, key2)
                        value = self.sudoku.grid_dict[key]
                        if value.click(pos[0], pos[1]):
                            self.isGridSelected = True
                            self.gridSelected = (key1, key2)
                            break


                if self.isGridSelected and event.type == pygame.KEYDOWN:
                    # fill in numbers
                    if self.gridSelected:
                        if event.key == pygame.K_1:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 1
                            self.sudoku.grid_dict[self.gridSelected].num = 1
                        if event.key == pygame.K_2:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 2
                            self.sudoku.grid_dict[self.gridSelected].num = 2
                        if event.key == pygame.K_3:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 3
                            self.sudoku.grid_dict[self.gridSelected].num = 3
                        if event.key == pygame.K_4:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 4
                            self.sudoku.grid_dict[self.gridSelected].num = 4
                        if event.key == pygame.K_5:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 5
                            self.sudoku.grid_dict[self.gridSelected].num = 5
                        if event.key == pygame.K_6:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 6
                            self.sudoku.grid_dict[self.gridSelected].num = 6
                        if event.key == pygame.K_7:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 7
                            self.sudoku.grid_dict[self.gridSelected].num = 7
                        if event.key == pygame.K_8:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 8
                            self.sudoku.grid_dict[self.gridSelected].num = 8
                        if event.key == pygame.K_9:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 9
                            self.sudoku.grid_dict[self.gridSelected].num = 9
                        if event.key == pygame.K_DELETE:
                            self.question[self.gridSelected[0]][self.gridSelected[1]] = 0
                            self.sudoku.grid_dict[self.gridSelected].num = 0

                    # move the selected grid
                    if event.key == pygame.K_UP:
                        if self.gridSelected[0] - 1 < 0:
                            self.gridSelected =  (8, self.gridSelected[1])
                        else:
                            self.gridSelected =  (self.gridSelected[0] - 1, self.gridSelected[1])

                    if event.key == pygame.K_DOWN:
                        if self.gridSelected[0] + 1 > 8:
                            self.gridSelected =  (0, self.gridSelected[1])
                        else:
                            self.gridSelected =  (self.gridSelected[0] + 1, self.gridSelected[1])

                    if event.key == pygame.K_LEFT:
                        if self.gridSelected[1] - 1 < 0:
                            self.gridSelected =  (self.gridSelected[0], 8)
                        else:
                            self.gridSelected =  (self.gridSelected[0] , self.gridSelected[1] - 1)

                    if event.key == pygame.K_RIGHT:
                        if self.gridSelected[1] + 1 > 8:
                            self.gridSelected =  (self.gridSelected[0], 0)
                        else:
                            self.gridSelected =  (self.gridSelected[0] , self.gridSelected[1] + 1)




            # draw the screen
            screen.fill((153, 255, 255))
            screen.blit(screen, (0,0))

            # draw sudoku
            self.sudoku.drawGrid(screen)
            self.sudoku.drawNum([], screen)

            # draw border for grid if a grid is selected
            if self.isGridSelected:
                self.sudoku.grid_dict[self.gridSelected].drawRect(screen, self.gridSelected[0], self.gridSelected[1])

            # draw buttons
            self.solve_btn.draw(screen)
            self.reset_btn.draw(screen)
            self.back_btn.draw(screen)

            # depends on whether the music is on or off
            if self.isMusic:
                self.sound_on_btn.draw(screen)

            else:
                self.sound_off_btn.draw(screen)


            # check whether it has a solution or not
            if self.isSolve:
                if self.sudoku.validQuestion(self.question) and self.sudoku.Solver((self.question)):
                    for i in range(9):
                        for j in range(9):
                            self.sudoku.grid_dict[(i, j)].num = self.question[i][j]
                    self.hasSolution = True
                else:
                    self.hasSolution = False
                self.isSolve = False
                self.showResult = True

            # tell player whether it has a solution or not
            if self.showResult:
                if self.hasSolution:
                    screen.blit(hasSol_text, (470 + large_button_img.get_width() // 2 - hasSol_text.get_width() // 2, 320))
                else:
                    screen.blit(noSol_text, (470 + large_button_img.get_width() // 2 - noSol_text.get_width() // 2, 320))

            pygame.display.flip()
            clock.tick(10)

