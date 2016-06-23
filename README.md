# Random-Crossword-Generator
This repo aims at generating crossword puzzle randomly and generating the corresponding LaTeX file, this code is used for NASIT 2016 bonquet of IT terminology puzzles.
## Python Crossword Generator
The main algorithm is from https://github.com/riverrun/genxword, I only modified to avoid 'upper-left' cross, which means one horizontal word and one vertical word have intersection on their first letter.
## Requirements:
As long as you can compile python code and LaTeX code
## How to use:
* First edit words.txt to modify word list, in the form 'word: clue for the word', notice that do not have an empty line in the end.
* The in terminal type 'python genxword.py', the code automatically generate the LaTeX file called 'Crossword.tex' for the newly generated crossword puzzle (If 'Crossword.tex' already exists, then it will be overwritten).
* Compile the .tex file and then you will have the .pdf file for the crossword, to switch between problem and solution, just comment / uncomment the line '\PuzzleSolution'
