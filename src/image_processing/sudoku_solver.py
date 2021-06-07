from argumentParser import parser
from digitExtractor import *
from cvFunctions import draw_sudoku



if __name__ == '__main__':
    #args = parser()
    #ex = Extractor(args.image, args.debug)
    DIR = 'sudoku.jpg'
    ex = Extractor(DIR)
    sudoku = ex.get_digits()

    for s in sudoku:
        print(s)

    random = np.random.randint(5, size=(9, 9))
    draw_sudoku(sudoku, random)
