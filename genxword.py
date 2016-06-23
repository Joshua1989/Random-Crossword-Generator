import sys, io, os

import random, time
from operator import itemgetter
from collections import defaultdict

class Crossword(object):
    def __init__(self, rows, cols, empty=' ', available_words=[]):
        self.rows = rows
        self.cols = cols
        self.empty = empty
        self.available_words = available_words
        self.let_coords = defaultdict(list)

    def prep_grid_words(self):
        self.current_wordlist = []
        self.let_coords.clear()
        self.grid = [[self.empty]*self.cols for i in range(self.rows)]
        self.available_words = [word[:2] for word in self.available_words]
        self.first_word(self.available_words[0])

    def compute_crossword(self, time_permitted=1.00):
        self.best_wordlist = []
        wordlist_length = len(self.available_words)
        time_permitted = float(time_permitted)
        start_full = float(time.time())
        while (float(time.time()) - start_full) < time_permitted:
            self.prep_grid_words()
            [self.add_words(word) for i in range(2) for word in self.available_words
             if word not in self.current_wordlist]
            if len(self.current_wordlist) > len(self.best_wordlist):
                self.best_wordlist = list(self.current_wordlist)
                self.best_grid = list(self.grid)
            if len(self.best_wordlist) == wordlist_length:
                break
        #answer = '\n'.join([''.join(['{} '.format(c) for c in self.best_grid[r]]) for r in range(self.rows)])
        answer = '\n'.join([''.join([u'{} '.format(c) for c in self.best_grid[r]])
                            for r in range(self.rows)])
        return answer + '\n\n' + str(len(self.best_wordlist)) + ' out of ' + str(wordlist_length)

    def get_coords(self, word):
        """Return possible coordinates for each letter."""
        word_length = len(word[0])
        coordlist = []
        temp_list =  [(l, v) for l, letter in enumerate(word[0])
                      for k, v in self.let_coords.items() if k == letter]
        for coord in temp_list:
            letc = coord[0]
            for item in coord[1]:
                (rowc, colc, vertc) = item
                if vertc:
                    if colc - letc >= 0 and (colc - letc) + word_length <= self.cols:
                        row, col = (rowc, colc - letc)
                        score = self.check_score_horiz(word, row, col, word_length)
                        if score:
                            coordlist.append([rowc, colc - letc, 0, score])
                else:
                    if rowc - letc >= 0 and (rowc - letc) + word_length <= self.rows:
                        row, col = (rowc - letc, colc)
                        score = self.check_score_vert(word, row, col, word_length)
                        if score:
                            coordlist.append([rowc - letc, colc, 1, score])
        if coordlist:
            return max(coordlist, key=itemgetter(3))
        else:
            return

    def first_word(self, word):
        """Place the first word at a random position in the grid."""
        vertical = random.randrange(0, 2)
        if vertical:
            row = random.randrange(0, self.rows - len(word[0]))
            col = random.randrange(0, self.cols)
        else:
            row = random.randrange(0, self.rows)
            col = random.randrange(0, self.cols - len(word[0]))
        self.set_word(word, row, col, vertical)

    def add_words(self, word):
        """Add the rest of the words to the grid."""
        coordlist = self.get_coords(word)
        if not coordlist:
            return
        row, col, vertical = coordlist[0], coordlist[1], coordlist[2]
        self.set_word(word, row, col, vertical)

    def check_score_horiz(self, word, row, col, word_length, score=1):
        cell_occupied = self.cell_occupied
        if col and cell_occupied(row, col-1) or col + word_length != self.cols and cell_occupied(row, col + word_length):
            return 0
        if row and (not cell_occupied(row-1, col) and cell_occupied(row, col) and (row+1 == self.rows or cell_occupied(row+1, col))):
            return 0
        if not row and cell_occupied(row, col):
        	return 0
        for letter in word[0]:
            active_cell = self.grid[row][col]
            if active_cell == self.empty:
                if row + 1 != self.rows and cell_occupied(row+1, col) or row and cell_occupied(row-1, col):
                    return 0
            elif active_cell == letter:
                score += 1
            else:
                return 0
            col += 1
        return score

    def check_score_vert(self, word, row, col, word_length, score=1):
        cell_occupied = self.cell_occupied
        if row and cell_occupied(row-1, col) or row + word_length != self.rows and cell_occupied(row + word_length, col):
            return 0
        if col and (not cell_occupied(row, col-1) and cell_occupied(row, col) and (col+1 == self.cols or cell_occupied(row, col+1))):
            return 0
        if not col and cell_occupied(row, col):
        	return 0
        for letter in word[0]:
            active_cell = self.grid[row][col]
            if active_cell == self.empty:
                if col + 1 != self.cols and cell_occupied(row, col+1) or col and cell_occupied(row, col-1):
                    return 0
            elif active_cell == letter:
                score += 1
            else:
                return 0
            row += 1
        return score

    def set_word(self, word, row, col, vertical):
        """Put words on the grid and add them to the word list."""
        word.extend([row, col, vertical])
        self.current_wordlist.append(word)

        horizontal = not vertical
        for letter in word[0]:
            self.grid[row][col] = letter
            if (row, col, horizontal) not in self.let_coords[letter]:
                self.let_coords[letter].append((row, col, vertical))
            else:
                self.let_coords[letter].remove((row, col, horizontal))
            if vertical:
                row += 1
            else:
                col += 1

    def cell_occupied(self, row, col):
        cell = self.grid[row][col]
        if cell == self.empty:
            return False
        else:
            return True

def crossword2tex(nrow, ncol, words):
    new_grid = [ [ '{} ' for _ in range(ncol) ] for _ in range(nrow) ]
    clues_across, clues_down = [], []
    for i, word in enumerate(words):
        r, c, v = words[i][2:]
        for j in range(len(words[i][0])):
            new_grid[r+v*j][c+(1-v)*j] = words[i][0][j].upper()
        if v == 0:
            clues_across.append( '\\Clue{{{0}}}{{{1}}}{{{2}}}'.format(i+1,words[i][0].upper(),words[i][1]) )
        else:
            clues_down.append( '\\Clue{{{0}}}{{{1}}}{{{2}}}'.format(i+1,words[i][0].upper(),words[i][1]) )
    for i, word in enumerate(words):
        r, c, v = words[i][2:]
        if new_grid[r][c][0] != '[':
            new_grid[r][c] = '[{0}]{1}'.format(i+1, new_grid[r][c])
    for r in range(nrow):
        for c in range(ncol):
            if r > 0 and r < nrow-1 and c > 0 and c < ncol-1:
                if new_grid[r][c][0] == '{' and new_grid[r-1][c][0] not in ['{','*']\
                    and new_grid[r+1][c][0] not in ['{','*'] and new_grid[r][c-1][0] not in ['{','*']\
                    and new_grid[r][c+1][0] not in ['{','*']:
                    new_grid[r][c] = '*  '
    text = '|' + '|.\n|'.join( [ '|'.join(line) for line in new_grid ] ) + '|.'
    return text, clues_across, clues_down



if __name__ == "__main__":
    ncol, nrow = 30, 30
    wordlist = [[line.split(':')[0].upper(), line.split(':')[1]] for line in open('words.txt').read().split('\n')]
    wordlist = wordlist[:]
    cw = Crossword(nrow, ncol, ' ', wordlist)
    print(cw.compute_crossword())

    text, clues_across, clues_down = crossword2tex(nrow, ncol, cw.best_wordlist)
    with open('Crosswords.tex','w') as out:
        out.write('\\documentclass[twoside]{article}'+"\n")
        # out.write('\\input{tex_macros}'+"\n")
        out.write('\\usepackage[unboxed,small]{cwpuzzle}'+"\n")

        out.write('\\begin{document}'+"\n")
        out.write('% \\PuzzleSolution'+"\n")
        out.write('\\begin{{Puzzle}}{{{0}}}{{{1}}}'.format(nrow,ncol)+"\n")
        out.write(text+"\n")
        out.write('\\end{Puzzle}'+"\n")

        out.write('\\newpage'+"\n")

        out.write('\\begin{PuzzleClues}{\\textbf{Across}}'+"\n\n")
        for line in clues_across:
            out.write(line+"\n\n")
        out.write('\\end{PuzzleClues}'+"\n\n")

        out.write('\\begin{PuzzleClues}{\\textbf{Down}}'+"\n\n")
        for line in clues_down:
            out.write(line+"\n\n")
        out.write('\\end{PuzzleClues}'+"\n\n")

        out.write('\\end{document}'+"\n")