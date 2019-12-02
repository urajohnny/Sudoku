import sys
import os
from collections import defaultdict

class SudokuError(Exception):
    def __init__(self, message):
        self.message = message

class Sudoku:
    def __init__(self, args):
        self.sudoku_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
        if not isinstance(args, str):
            raise SudokuError('Incorrect input')
        else:
            with open(args, encoding = "utf-8") as sudoku:
                sudoku_matrix = [[]] * 9
                sudoku_colum = []
                count_line, box_number = 0, 0
                box = []
                for line in sudoku:
                    if not list(line.split()):
                        continue
                    sudoku_matrix[count_line] = [e for e in line.strip().replace(' ', '')] #store in sudoku_matrix
                    #sudoku_matrix[count_line] = list(sudoku_matrix[count_line])
                    count_line += 1
            if count_line != 9:
                raise SudokuError('Incorrect input')
            # check column and row, then store in sudoku_colum
            for i in range(9):
                L = []
                if len(sudoku_matrix[i]) != 9:
                    raise SudokuError('Incorrect input')
                if self.incorrect(sudoku_matrix[i]):
                    raise SudokuError('Incorrect input')
                for j in range(9):
                    L.append(sudoku_matrix[j][i])
                sudoku_colum.append(L)
            # store in box
            while box_number <= 8:
                L = []
                if box_number < 3:
                    for i in range(3):
                        for j in range(3 * box_number, 3 * box_number +3):
                            L.append(sudoku_matrix[i][j])
                elif box_number < 6:
                    for i in range(3, 6):
                        for j in range(3 * (box_number - 3), 3 * (box_number - 3) +3):
                            L.append(sudoku_matrix[i][j])
                else:
                    for i in range(6, 9):
                        for j in range(3 * (box_number - 6), 3 * (box_number - 6) +3):
                            L.append(sudoku_matrix[i][j])
                box_number += 1
                box.append(L)
            self.args = args
            self.sudoku_matrix = sudoku_matrix
            self.sudoku_colum = sudoku_colum
            self.box = box

    def duplicate(self, L):
        for e in L:
            if L.count(e) > 1 and e != '0':
                return True
        return False

    def incorrect(self, L):
        for e in L:
            if e < '0' or e > '9':
                return True
        return False

    def preassess(self):
        # check every number in a box, column and row repeated or not
        for i in range(9):
            if self.duplicate(self.box[i]):
                print('There is clearly no solution.')
                return
            if self.duplicate(self.sudoku_matrix[i]):
                print('There is clearly no solution.')
                return
            if self.duplicate(self.sudoku_colum[i]):
                print('There is clearly no solution.')
                return
        print('There might be a solution.')
        return

    def bare_tex_output(self):
        bare_tex = open(self.args.strip('.txt') + '_bare.tex', 'w')
        self.printhead_into_file(bare_tex)
        for i in range(9):
            bare_tex.write(f'\n% Line {i + 1}\n')
            for j in range(9):
                if self.sudoku_matrix[i][j] != '0':
                    bare_tex.write('\\N{}{}{}{}{'f'{self.sudoku_matrix[i][j]}''} ')
                else:
                    bare_tex.write('\\N{}{}{}{}{} ')
                if j == 8:
                    bare_tex.write('\\\ \\hline')
                elif j % 3 == 2:
                    bare_tex.write('&\n')
                else:
                    bare_tex.write('& ')
            if i % 3 == 2:
                bare_tex.write('\\hline')
            bare_tex.write('\n')
        self.printfoot_into_file(bare_tex)

    def printhead_into_file(self, arg):
        arg.write('\documentclass[10pt]{article}\n\\usepackage[left=0pt,right=0pt]{geometry}'
                  '\n\\usepackage{tikz}\n\\usetikzlibrary{positioning}\n\\usepackage{cancel}\n\\pagestyle{empty}'
                  '\n\n\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},'
                  '\n                               label=above right:{\\tiny #2},'
                  '\n                               label=below left:{\\tiny #3},'
                  '\n                               label=below right:{\\tiny #4}]{#5};}}'
                  '\n\n\\begin{document}'
                  '\n\n\\tikzset{every node/.style={minimum size=.5cm}}\n\n\\begin{center}'
                  '\n\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\\hline\\hline')

    def printfoot_into_file(self, arg):
        arg.write('\\end{tabular}'
                  '\n\\end{center}'
                  '\n'
                  '\n\\end{document}\n')

    def forced_tex(self):
        while True:
            box_available = [{}] * 9
            has_forced = False
            for i in range(9):
                box_available[i] = self.sudoku_set - set(self.box[i])
                for e in box_available[i]:
                    count_available = 0
                    for j in range(9):
                        if self.box[i][j] == '0':
                            if e in self.sudoku_matrix[i // 3 * 3 + j // 3] or e in self.sudoku_colum[(i % 3) * 3 + j % 3]:
                                continue
                            else:
                                count_available += 1
                                available_i = i
                                available_j = j
                                if count_available >= 2:
                                    break
                    if count_available == 1:
                        self.box[available_i][available_j] = e
                        self.sudoku_matrix[available_i // 3 * 3 + available_j // 3][(available_i % 3) * 3 + available_j % 3] = e
                        self.sudoku_colum[(available_i % 3) * 3 + available_j % 3][available_i // 3 * 3 + available_j // 3] = e
                        has_forced = True
            if not has_forced:
                break


    def forced_tex_output(self):
        self.forced_tex()
        forced_tex = open(self.args.strip('.txt') + '_forced.tex', 'w')
        self.printhead_into_file(forced_tex)
        for i in range(9):
            forced_tex.write(f'\n% Line {i + 1}\n')
            for j in range(9):
                if self.sudoku_matrix[i][j] != '0':
                    forced_tex.write('\\N{}{}{}{}{'f'{self.sudoku_matrix[i][j]}''} ')
                else:
                    forced_tex.write('\\N{}{}{}{}{} ')
                if j == 8:
                    forced_tex.write('\\\ \\hline')
                elif j % 3 == 2:
                    forced_tex.write('&\n')
                else:
                    forced_tex.write('& ')
            if i % 3 == 2:
                forced_tex.write('\\hline')
            forced_tex.write('\n')
        self.printfoot_into_file(forced_tex)

    def marked_tex(self):
        self.forced_tex()
        box_available = [[{} for _ in range(9)] for _ in range(9)]
        self.matrix_available = [[[] for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if self.box[i][j] == '0':
                    box_available[i][j] = self.sudoku_set - set(self.box[i]) \
                                         - set(self.sudoku_matrix[i // 3 * 3 + j // 3]) \
                                         - set(self.sudoku_colum[(i % 3) * 3 + j % 3])
                    self.matrix_available[i // 3 * 3 + j // 3][(i % 3) * 3 + j % 3] = [int(x) for x in box_available[i][j]]

    def marked_tex_output(self):
        self.marked_tex()
        # print(matrix_available)
        marked_tex = open(self.args.strip('.txt') + '_marked.tex', 'w')
        self.print_marked_into_file(marked_tex)

    def print_marked_into_file(self,arg):
        self.printhead_into_file(arg)
        for i in range(9):
            arg.write(f'\n% Line {i + 1}\n')
            for j in range(9):
                marked_str = '{'
                topleft, topright, lowerleft, lowerright = [], [], [], []
                if self.matrix_available[i][j] != {}:
                    self.matrix_available[i][j].sort()
                    for e in self.matrix_available[i][j]:
                        if e <= 2:
                            topleft.append(e)
                        elif e <= 4:
                            topright.append(e)
                        elif e <= 6:
                            lowerleft.append(e)
                        else:
                            lowerright.append(e)
                arg.write('\\N')
                for e in topleft:
                    if len(topleft) == 2 and e == 2:
                        marked_str += ' '
                    marked_str += str(e)
                marked_str += '}{'
                for e in topright:
                    if len(topright) == 2 and e == 4:
                        marked_str += ' '
                    marked_str += str(e)
                marked_str += '}{'
                for e in lowerleft:
                    if len(lowerleft) == 2 and e == 6:
                        marked_str += ' '
                    marked_str += str(e)
                marked_str += '}{'
                for e in range(len(lowerright)):
                    if e >= 1:
                        marked_str += ' '
                    marked_str += str(lowerright[e])
                marked_str += '}'
                # print(marked_str)
                arg.write(marked_str)
                if self.sudoku_matrix[i][j] != '0':
                    arg.write('{'f'{self.sudoku_matrix[i][j]}''} ')
                else:
                    arg.write('{} ')
                if j == 8:
                    arg.write('\\\ \\hline')
                elif j % 3 == 2:
                    arg.write('&\n')
                else:
                    arg.write('& ')
            if i % 3 == 2:
                arg.write('\\hline')
            arg.write('\n')
        self.printfoot_into_file(arg)

    def worked_tex(self):
        self.marked_tex()
        preemptive_set = [[[] for _ in range(9)] for _ in range(9)]
        #used to check whether there is a change
        current_matrix_available = []
        self.copy_matrix_available = [[y for y in x] for x in self.matrix_available]
        while True:
            self.change = False
            for i in range(9):
                for j in range(9):
                    # print(self.matrix_available[i][j])
                    x = 0
                    for e in self.copy_matrix_available[i][j]:
                        x |= 1 << (e - 1)
                    preemptive_set[i][j] = [x, len(self.copy_matrix_available[i][j])]
            # print(preemptive_set)
            self.check_row(preemptive_set)
            self.check_colum(preemptive_set)
            self.check_box(preemptive_set)
            if self.copy_matrix_available == current_matrix_available:
                break
            # print(self.copy_matrix_available)
            current_matrix_available = [[y for y in x] for x in self.copy_matrix_available]
        for i in range(9):
            for j in range(9):
                if len(self.copy_matrix_available[i][j]) == 1:
                    for e in self.copy_matrix_available[i][j]:
                        self.sudoku_matrix[i][j] = str(e)
                    self.copy_matrix_available[i][j].pop()
        # print(self.sudoku_matrix)

    def worked_tex_output(self):
        self.worked_tex()
        # print(self.sudoku_matrix)
        worked_tex = open(self.args.strip('.txt') + '_worked.tex', 'w')
        self.printhead_into_file(worked_tex)
        for i in range(9):
            worked_tex.write(f'\n% Line {i + 1}\n')
            for j in range(9):
                marked_str = '{'
                topleft, topright, lowerleft, lowerright = [], [], [], []
                if self.matrix_available[i][j] != {}:
                    self.matrix_available[i][j].sort()
                    for e in self.matrix_available[i][j]:
                        if e <= 2:
                            topleft.append(e)
                        elif e <= 4:
                            topright.append(e)
                        elif e <= 6:
                            lowerleft.append(e)
                        else:
                            lowerright.append(e)
                worked_tex.write('\\N')
                for e in topleft:
                    if len(topleft) == 2 and e == 2:
                        marked_str += ' '
                    if e not in self.copy_matrix_available[i][j]:
                        marked_str += str('\cancel{'f'{e}''}')
                    else:
                        marked_str += str(e)
                marked_str += '}{'
                for e in topright:
                    if len(topright) == 2 and e == 4:
                        marked_str += ' '
                    if e not in self.copy_matrix_available[i][j]:
                        marked_str += str('\cancel{'f'{e}''}')
                    else:
                        marked_str += str(e)
                    # marked_str += str(e)
                marked_str += '}{'
                for e in lowerleft:
                    if len(lowerleft) == 2 and e == 6:
                        marked_str += ' '
                    if e not in self.copy_matrix_available[i][j]:
                        marked_str += str('\cancel{'f'{e}''}')
                    else:
                        marked_str += str(e)
                marked_str += '}{'
                for e in range(len(lowerright)):
                    if e >= 1:
                        marked_str += ' '
                    if lowerright[e] not in self.copy_matrix_available[i][j]:
                        marked_str += str('\cancel{'f'{lowerright[e]}''}')
                    else:
                        marked_str += str(lowerright[e])
                    # marked_str += str(lowerright[e])
                marked_str += '}'
                # print(marked_str)
                worked_tex.write(marked_str)
                if self.sudoku_matrix[i][j] != '0':
                    worked_tex.write('{'f'{self.sudoku_matrix[i][j]}''} ')
                else:
                    worked_tex.write('{} ')
                if j == 8:
                    worked_tex.write('\\\ \\hline')
                elif j % 3 == 2:
                    worked_tex.write('&\n')
                else:
                    worked_tex.write('& ')
            if i % 3 == 2:
                worked_tex.write('\\hline')
            worked_tex.write('\n')
        self.printfoot_into_file(worked_tex)


    def check_row(self,preemptive_set):
        for i in range(9):
            for j in range(9):
                if not preemptive_set[i][j][1]:
                    continue
                count_set = 0
                for y in range(9):
                    if preemptive_set[i][y][1] != 0 and preemptive_set[i][y][0] | preemptive_set[i][j][0] == \
                            preemptive_set[i][j][0]:
                        count_set += 1
                if count_set == preemptive_set[i][j][1]:
                    for y in range(9):
                        if preemptive_set[i][y][0] | preemptive_set[i][j][0] != preemptive_set[i][j][0]:
                            preemptive_set[i][y][0] &= (511 - preemptive_set[i][j][0])
                            self.copy_matrix_available[i][y] = self.convert_number_to_list(preemptive_set[i][y][0])


    def check_colum(self, preemptive_set):
        for j in range(9):
            for i in range(9):
                if not preemptive_set[i][j][1]:
                    continue
                count_set = 0
                for x in range(9):
                    if preemptive_set[x][j][1] != 0 and preemptive_set[x][j][0] | preemptive_set[i][j][0] == \
                            preemptive_set[i][j][0]:
                        count_set += 1
                if count_set == preemptive_set[i][j][1]:
                    for x in range(9):
                        if preemptive_set[x][j][0] | preemptive_set[i][j][0] != preemptive_set[i][j][0]:
                            preemptive_set[x][j][0] &= (511 - preemptive_set[i][j][0])
                            self.copy_matrix_available[x][j] = self.convert_number_to_list(preemptive_set[x][j][0])


    def check_box(self,preemptive_set):
        for i in range(9):
            for j in range(9):
                if not preemptive_set[i // 3 * 3 + j // 3][i % 3 * 3 + j % 3][1]:
                    continue
                count_set = 0
                for y in range(9):
                    if preemptive_set[i // 3 * 3 + y // 3][i % 3 * 3 + y % 3][1] != 0 and preemptive_set[i // 3 * 3 + y // 3][i % 3 * 3 + y % 3][0] |\
                            preemptive_set[i // 3 * 3 + j // 3][i % 3 * 3 + j % 3][0] == \
                            preemptive_set[i // 3 * 3 + j // 3][i % 3 * 3 + j % 3][0]:
                        count_set += 1
                if count_set == preemptive_set[i // 3 * 3 + j // 3][i % 3 * 3 + j % 3][1]:
                    for y in range(9):
                        if preemptive_set[i // 3 * 3 + y // 3][i % 3 * 3 + y % 3][0] |\
                            preemptive_set[i // 3 * 3 + j // 3][i % 3 * 3 + j % 3][0] != \
                                preemptive_set[i // 3 * 3 + j // 3][i % 3 * 3 + j % 3][0]:
                            preemptive_set[i // 3 * 3 + y // 3][i % 3 * 3 + y % 3][0] &= (511 - preemptive_set[i // 3 * 3 + j // 3][i % 3 * 3 + j % 3][0])
                            self.copy_matrix_available[i // 3 * 3 + y // 3][i % 3 * 3 + y % 3] = self.convert_number_to_list(preemptive_set[i // 3 * 3 + y // 3][i % 3 * 3 + y % 3][0])


    def convert_number_to_list(self, x):
        L = []
        n = 1
        while x:
            if x & 1:
                L.append(n)
            x >>= 1
            n += 1
        return L
