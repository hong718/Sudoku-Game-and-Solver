import pygame
import os
import random
from grid import Grid
from _collections import defaultdict, OrderedDict


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
text_font = pygame.font.Font(os.path.join('game_assets','Boba.otf'), 80)
warning_font = pygame.font.Font(os.path.join('game_assets','Boba.otf'), 30)

# loading_font
loading_font1 = text_font.render('Loading', True, (0, 0, 0))
loading_font2 = text_font.render('Loading .', True, (0, 0, 0))
loading_font3 = text_font.render('Loading . .', True, (0, 0, 0))
loading_font4 = text_font.render('Loading . . .', True, (0, 0, 0))
loading_font = [loading_font1, loading_font2, loading_font3, loading_font4]
warning_text = warning_font.render('It may take a longer time to load a difficult puzzle :)', True, (0, 0 ,0))


class Sudoku():
    def __init__(self, x, y, sudoku = None):
        self.x = x
        self.y = y
        self.count = 0
        self.sudoku = sudoku
        self.width = 42
        self.grid_dict = {}
        self.isMulSol = None
        self.search = 0
        self.question_index = set()
        self.ans = []
        self.test = 0

    def genQuestion(self, difficulty, screen):
        '''
        return a sudoku question with required difficulty
        :param difficulty: str, surface
        :return: list[list], set, list[list]
        '''

        # set the difficulty
        # first metric is the number of given cells
        # second metric is lower bound of given cells in each row and column
        # third metric is the searchTime
        nonzeroNum_dict = OrderedDict()
        nonzeroNum_dict[50] = 1
        nonzeroNum_dict[36] = 2
        nonzeroNum_dict[32] = 3
        nonzeroNum_dict[28] = 4
        nonzeroNum_dict[22] = 5

        lowerBound_dict = OrderedDict()
        lowerBound_dict[5] = 1
        lowerBound_dict[4] = 2
        lowerBound_dict[3] = 3
        lowerBound_dict[2] = 4
        lowerBound_dict[0] = 5

        searchTime_dict = OrderedDict()
        searchTime_dict[100000] = 5
        searchTime_dict[10000] = 4
        searchTime_dict[1000] = 3
        searchTime_dict[100] = 2
        searchTime_dict[0] = 1


        if difficulty == 'easy':
            scoreRange = range(3, 8)
        elif difficulty == 'medium':
            scoreRange = range(8, 12)
        elif difficulty == 'difficult':
            scoreRange = range(12, 16)


        # keep generating a sudoku question until the difficulty requirements are satisfied
        load_count = 0
        score = 0
        while score not in scoreRange:
            score = 0
            # show loading screen
            screen.fill((153, 255, 255))
            if load_count > 3:
                load_count = 0
            screen.blit(loading_font[load_count], (360 - loading_font4.get_width() // 2, 240 - loading_font4.get_height() // 2))
            screen.blit(warning_text, (360 - warning_text.get_width() // 2, 400))

            # obtain a finished sudoku
            QuestionBoard = self.genFullBoard()
            self.ans = []
            for i in range(9):
                self.ans.append(QuestionBoard[i][:])

            # obtain a random list of index
            index_list = []
            for i in range(9):
               for j in range(9):
                   index_list.append([i, j])
            random.shuffle(index_list)

            # find a question board with unique solution by eliminating cells from a finished sudoku board
            self.search = 0
            for index in index_list:
                self.count = 0
                self.isMulSol = False
                tmp = QuestionBoard[index[0]][index[1]]
                QuestionBoard[index[0]][index[1]] = 0
                self.ansSolver(QuestionBoard)
                if not self.isMulSol:
                    continue
                else:
                    QuestionBoard[index[0]][index[1]] = tmp
                    # calculate the difficulty
                    for key, value in nonzeroNum_dict.items():
                        if self.nonZero(QuestionBoard) >= key:
                            score += value
                            break
                    for key, value in lowerBound_dict.items():
                        if self.lowerBound(QuestionBoard) >= key:
                            score += value
                            break
                    for key, value in searchTime_dict.items():
                        if self.search >= key:
                            score += value
                            break
                    break

            load_count += 1
            pygame.display.flip()
            clock.tick(2)

        # Save the index for given cells at the beginning
        # Make a Grid object for each index
        self.question_index = set()
        for i in range(9):
            for j in range(9):
                if QuestionBoard[i][j] != 0:
                    self.question_index.add((i, j))
                self.grid_dict[(i, j)] = Grid(i, j, QuestionBoard[i][j])

        return QuestionBoard, self.question_index, self.ans

    def genFullBoard(self):
        '''
        generate a random sudoku according to the request
        :return: none
        '''
        fullBoard = []
        for i in range(9):
            fullBoard.append([0] * 9)
        self.Solver(fullBoard, 1)
        return fullBoard

    def findEmpty(self, sudoku):
         '''
         find the first '0' entry
         :param sudoku: list[list]
         :param empty: list[int]
         :return: tuple
         '''
         for row in range(9):
             for col in range(9):
                    if sudoku[row][col] == 0:
                         return (row, col)

    def valid(self, sudoku, empty, num):
         '''
         check whether a number can put into a empty box
         :param sudoku: list[list]
         :param empty: list[int]
         :param num: int
         :return: bool
         '''

         for i in range(9):
             # check whether the number is used in the row
             if sudoku[empty[0]][i] == num and (empty[0], i) != empty:
                 return False
             # check whether the number is used in the col
             if sudoku[i][empty[1]] == num and (i, empty[1]) != empty:
                 return False

         # check whether the number is used in the box
         for i in range(empty[0] // 3 * 3, empty[0] // 3 * 3 + 3):
             for j in range(empty[1] // 3 * 3, empty[1] // 3 * 3 + 3):
                 if sudoku[i][j] == num and (i, j) != empty:
                     return False

         return True

    def ansSolver(self, sudoku):
        '''
        check whether there are multiple solutions
        :param sudoku: list[list]
        :return: None
        '''

        # if more then two solutions are found, bool turns True and skip the later backtracking
        if self.count >= 2:
            self.isMulSol = True
            return

        # count number of trials needed
        if self.count <= 1:
            self.search += 1
        empty = self.findEmpty(sudoku)


        # if a board is finished, counter += 1
        if empty is None:
            self.count += 1
            return
        else:
            row, col = empty[0], empty[1]

        # backtracking
        for num in range(1, 10):
            if self.valid(sudoku, (row, col), num):
                sudoku[row][col] = num
                self.ansSolver(sudoku)
                sudoku[row][col] = 0

    def Solver(self, sudoku, index = 0):
        '''
        solve a sudoku by backtracking, if index = 1, randomize the guesses, else in ascending order
        :param sudoku: list[list]
        :param index: int
        :return: None
        '''

        empty = self.findEmpty(sudoku)

        if not empty:
            return True
        else:
            row, col = empty[0], empty[1]
        if index == 1:
            # randomize guesses
            number = list(range(1,10))
            random.shuffle(number)
        else:
            number = range(1, 10)
        for num in number:
            if self.valid(sudoku, (row,col), num):
                sudoku[row][col] = num
                if self.Solver(sudoku, index):
                    return True
                sudoku[row][col] = 0
        return False

    def validQuestion(self, sudoku):
        '''
        check whether a sudoku question is valid
        :param sudoku: list[list]
        :return: bool
        '''
        # save the numbers in corresponding rows, columns and grid
        dr = defaultdict(list)
        dc = defaultdict(list)
        dg = defaultdict(list)

        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    continue
                else:
                    gi = (i // 3) * 3 + j // 3
                # check whether the number is in its row / column / grid
                if sudoku[i][j] in dr[(i, 0)] or sudoku[i][j] in dc[(0, j)] or sudoku[i][j] in dg[gi]:
                    return False
                # add the number in its row / column / grid
                dr[(i,0)].append(sudoku[i][j])
                dc[(0,j)].append(sudoku[i][j])
                dg[gi].append(sudoku[i][j])
        return True

    def genEmpty(self):
        '''
        generate an empty board
        :return: None
        '''
        for i in range(9):
            for j in range(9):
                self.grid_dict[(i, j)] = Grid(i, j, 0)

    def lowerBound(self, sudoku):
        '''
        Calculate the lower bound of given cells in rows and columns
        :param sudoku: list[list]
        :return: int
        '''

        lowerbound = 9
        for i in range(9):
            nonzeroNum = 0
            for j in range(9):
                if sudoku[i][j] != 0:
                    nonzeroNum += 1
            if lowerbound > nonzeroNum:
                lowerbound = nonzeroNum
        for i in range(9):
            nonzeroNum = 0
            for j in range(9):
                if sudoku[j][i] != 0:
                    nonzeroNum += 1
            if lowerbound > nonzeroNum:
                lowerbound = nonzeroNum
        return lowerbound

    def nonZero(self, sudoku):
        '''
        Calculate number of given cells in a question sudoku
        :param sudoku: list[list]
        :return: int
        '''
        nonzeroNum = 0
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] != 0:
                    nonzeroNum += 1
        return nonzeroNum

    def drawGrid(self, win):
        '''
        draw the grid line of a sudoku
        :param win: Surface
        :return: None
        '''
        for i in range(10):
            if i % 3 != 0:
              pygame.draw.line(win, (128, 128, 128), (self.x + self.width * i, self.y), (self.x + self.width * i, self.y + self.width * 9), 2)
              pygame.draw.line(win, (128, 128, 128), (self.x, self.y + self.width * i), (self.x + self.width * 9, self.y + self.width * i), 2)
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(win, (0, 0, 0), (self.x + self.width * i, self.y), (self.x + self.width * i, self.y + self.width * 9), 3)
                pygame.draw.line(win, (0, 0, 0), (self.x, self.y + self.width * i), (self.x + self.width * 9, self.y + self.width * i), 3)

    def drawNum(self, question_index, win):
        '''
        draw the numbers
        :param question_index: set()
        :param win: Surface
        :return: None
        '''
        # draw given cells in black
        # draw player input in blue
        for key1, key2 in self.grid_dict:
            key = (key1, key2)
            value = self.grid_dict[key]
            if value.num != 0 and key in question_index:
                value.draw(win, (0, 0, 0))
            elif value.num != 0 and key not in question_index:
                value.draw(win, (0, 0, 255))
