import numpy as np

from argumentParser import parser
from digitExtractor import Extractor
from cvFunctions import draw_sudoku
from keras.models import load_model
from src.modeling.evaluating import solve_human_approach, transform


if __name__ == '__main__':
    args = parser()
    ex = Extractor(args.image, args.debug)
    unsolved = ex.get_digits()

    model = load_model('../sudoku_models/CNN.hp5')

    sudoku = transform(unsolved)
    predict = solve_human_approach(sudoku, model).astype(np.uint8)

    draw_sudoku(unsolved, predict)
