import pygame
import sys
import os
from button import Button
from sudoku import Sudoku

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()
time_font = pygame.font.Font(os.path.join('game_assets', 'Boba.otf'), 30)

# button_img
large_button_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','button.png')), (200, 60))
back_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','back.png')), (60, 60))
sound_on_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','sound_on.png')), (60, 60))
sound_off_img = pygame.transform.scale(pygame.image.load(os.path.join('game_assets','sound_off.png')), (60, 60))

# font
text_font = pygame.font.Font(os.path.join('game_assets','Boba.otf'), 40)
fail_text = text_font.render('It is incorrect!', True, (0, 0, 0))
correct_text = text_font.render('Correct!', True, (0, 0, 0))


class gameScreen:
    def __init__(self, difficulty):
        self.second = 0
        self.min = 0
        self.hour = 0
        self.sudoku = Sudoku(30, 60)
        self.hint_btn = Button(large_button_img, 480, 95, 30, 'Hint')
        self.sol_btn = Button(large_button_img, 480, 170, 30, 'Solution')
        self.regen_btn = Button(large_button_img, 480, 245, 30, 'Regenerate')
        self.submit_btn = Button(large_button_img, 480, 320, 30, 'Submit')
        self.back_btn = Button(back_img, 650, 20)
        self.sound_on_btn = Button(sound_on_img, 580, 20)
        self.sound_off_btn = Button(sound_off_img, 580, 20)
        self.isMusic = True
        self.gen = True
        self.isSolution = False
        self.isHint = False
        self.isSubmit = False
        self.player = []
        self.ans = []
        self.question_index = None
        self.isGridSelected = False
        self.gridSelected = None
        self.isCorrect = None
        self.difficulty = difficulty
        self.curr_time = 0
        self.isRun = True
        self.count_time = True

    def run(self):
        while self.isRun:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.isSubmit = False
                    # check whether the music button is clicked
                    if self.isMusic and self.sound_on_btn.click(pos[0], pos[1]):
                        pygame.mixer.music.pause()
                        self.isMusic = False
                    elif not self.isMusic and self.sound_off_btn.click(pos[0], pos[1]):
                        pygame.mixer.music.unpause()
                        self.isMusic = True

                    # check whether the back button is clicked
                    if self.back_btn.click(pos[0], pos[1]):
                        self.isRun = False

                    # check whether the solution button is clicked
                    if self.sol_btn.click(pos[0], pos[1]):
                        self.isSolution = True

                    # check whether the hint button is clicked
                    if self.hint_btn.click(pos[0],pos[1]) and self.player != self.ans:
                        self.isHint = True

                    # check whether the regenerate button is clicked
                    if self.regen_btn.click(pos[0], pos[1]):
                        self.gen = True

                    # check whether the submit button is clicked
                    if self.submit_btn.click(pos[0], pos[1]):
                        self.isSubmit = True
                        if self.player == self.ans:
                            self.isCorrect = True
                            self.count_time = False
                        else:
                            self.isCorrect = False

                    # check whether the grid is clicked
                    for key1, key2 in self.sudoku.grid_dict:
                        key = (key1, key2)
                        value = self.sudoku.grid_dict[key]
                        if value.click(pos[0], pos[1]) and key not in self.question_index:
                            self.isGridSelected = True
                            self.gridSelected = (key1, key2)
                            break


                if self.isGridSelected and event.type == pygame.KEYDOWN:
                    # fill in numbers
                    if self.gridSelected not in self.question_index:
                        if event.key == pygame.K_1:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 1
                            self.sudoku.grid_dict[self.gridSelected].num = 1
                        if event.key == pygame.K_2:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 2
                            self.sudoku.grid_dict[self.gridSelected].num = 2
                        if event.key == pygame.K_3:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 3
                            self.sudoku.grid_dict[self.gridSelected].num = 3
                        if event.key == pygame.K_4:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 4
                            self.sudoku.grid_dict[self.gridSelected].num = 4
                        if event.key == pygame.K_5:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 5
                            self.sudoku.grid_dict[self.gridSelected].num = 5
                        if event.key == pygame.K_6:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 6
                            self.sudoku.grid_dict[self.gridSelected].num = 6
                        if event.key == pygame.K_7:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 7
                            self.sudoku.grid_dict[self.gridSelected].num = 7
                        if event.key == pygame.K_8:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 8
                            self.sudoku.grid_dict[self.gridSelected].num = 8

                        if event.key == pygame.K_9:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 9
                            self.sudoku.grid_dict[self.gridSelected].num = 9
                        if event.key == pygame.K_DELETE:
                            self.player[self.gridSelected[0]][self.gridSelected[1]] = 0
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


            # draw screen
            screen.fill((153, 255, 255))
            screen.blit(screen, (0,0))

            # draw sudoku grid line
            self.sudoku.drawGrid(screen)

            # draw the sudoku
            if self.gen:
                self.player, self.question_index, self.ans = self.sudoku.genQuestion(self.difficulty, screen)
                self.gen = False
                self.curr_time = pygame.time.get_ticks()
                self.count_time = True

            self.sudoku.drawNum(self.question_index, screen)

            # draw hint
            if self.isHint:
                empty = self.sudoku.findEmpty(self.player)
                self.player[empty[0]][empty[1]] = self.ans[empty[0]][empty[1]]
                self.sudoku.grid_dict[empty].num = self.ans[empty[0]][empty[1]]
                self.isHint = False

            # draw border for grid if a grid is selected
            if self.isGridSelected:
                self.sudoku.grid_dict[self.gridSelected].drawRect(screen, self.gridSelected[0], self.gridSelected[1])


            # draw solution
            if self.isSolution:
                for i in range(9):
                    for j in range(9):
                        self.player[i][j] = self.ans[i][j]
                for i in range(9):
                    for j in range(9):
                        self.sudoku.grid_dict[(i, j)].num = self.ans[i][j]
                self.isSolution = False


            # show result
            if self.isSubmit and self.isCorrect:
                screen.blit(correct_text, (480 + large_button_img.get_width() // 2 - correct_text.get_width() // 2, 390))
            elif self.isSubmit and not self.isCorrect:
                screen.blit(fail_text, (480 + large_button_img.get_width() // 2 - fail_text.get_width() // 2, 390))



            # draw button
            self.hint_btn.draw(screen)
            self.sol_btn.draw(screen)
            self.regen_btn.draw(screen)
            self.submit_btn.draw(screen)
            self.back_btn.draw(screen)

            # depends on whether the music is on or off
            if self.isMusic:
                self.sound_on_btn.draw(screen)
            else:
                self.sound_off_btn.draw(screen)

            # show timer
            if self.count_time:
                (self.hour, self.min, self.second) = self.get_time(self.curr_time)
            self.draw_time(self.hour, self.min, self.second, screen)



            pygame.display.flip()
            clock.tick(20)

    def get_time(self, curr_time):
        '''
        record the curr time
        :return: a tuple of curr time
        '''
        mseconds = pygame.time.get_ticks() - curr_time
        seconds = mseconds // 1000
        mins = seconds // 60
        seconds -= 60 * mins
        hours = mins // 24
        mins -= 60 * hours
        return (hours, mins, seconds)

    def draw_time(self, hour, min, second, win):
        '''
        draw the timer on the left-hand top corner
        :param hour: int
        :param min: int
        :param second: int
        :param win: surface
        :return: none
        '''
        if hour < 10:
            shour = '0' + str(hour)
        else:
            shour = str(hour)

        if min < 10:
            smin = '0' + str(min)
        else:
            smin = str(min)
        if second < 10:
            ssecond= '0' + str(second)
        else:
            ssecond = str(second)
        time = time_font.render(shour + ':' + smin + ':' + ssecond, True, (0, 0, 0))
        win.blit(time, (20,10))
