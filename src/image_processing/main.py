import numpy as np

from argumentParser import parser
from shapeExtractor import *



if __name__ == '__main__':
    #args = parser()
    #ex = Extractor(args.image, args.debug)
    DIR = 'sudoku.jpg'
    ex = Extractor(DIR)
    sudoku = ex.get_digits()

    print(type(sudoku))
    for s in sudoku:
        print(s)




