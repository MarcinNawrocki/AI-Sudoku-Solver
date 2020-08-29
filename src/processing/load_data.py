import copy

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split

def get_data(number_of_samples = 300000, approach=1):
    """Loading data with sudoku boards from file and split it into  training and  test datasets using function for sklearn

    Keyword Arguments:
        number_of_samples {int} -- number of samples to load (default: {300000})
        approach {int} -- specifies for which approach data should be loaded (possible values: 1 or 2) (default: {1})

    Returns:
        [tuple of NumPy arrays] -- (X_train, X_test, y_train, y_test)
    """
    np_X, np_y = load_from_file(number_of_samples, approach,0)

    X_train, X_test, y_train, y_test = train_test_split(np_X, np_y, test_size=0.2)

    return X_train, X_test, y_train, y_test


def get_test_examples(number_of_examples):
    """Loading new sudoku boards to evaluate model

    Arguments:
        number_of_examples {int} -- specifies the number of exaples to load

    Returns:
        [tuple of NumPy arrays] -- two arrays containing unsolved and solved test samples
    """
    number_of_sudokus = 1000000
    start_row = number_of_sudokus - number_of_sudokus
    np_X, np_y = load_from_file(number_of_examples, 1, start_row)

    return np_X, np_y

def load_from_file(number_of_samples, approach, start_row=0):
    """Load specified number of sudoku boards, starting with specified row

    Arguments:
        number_of_samples {int} -- [description]
        approach {int} -- specifies for which approach data should be loaded (possible values: 1 or 2) (default: {1})

    Keyword Arguments:
        start_row {int} -- [description] (default: {0})

    Returns:
        [tuple of NumPy arrays] -- two arrays containing unsolved and solved sudoku samples
    """
    df = pd.read_csv("./data/sudoku.csv")
    last_row = start_row+number_of_samples

    unsolved = df['quizzes'].iloc[start_row:last_row].values
    solved = df['solutions'].iloc[start_row:last_row].values

    X=[]
    y=[]
    #generate NumPy arrays
    if (approach == 1):
        for sudoku in unsolved:
            np_unsolved = np.array([int(x) for x in sudoku]).reshape(9,9,1)
            X.append(np_unsolved)
    
    for sudoku in solved:
        np_solved = np.array([int(y) for y in sudoku]).reshape(81,1) -1
        y.append(np_solved)
        if approach == 2:
            np_solved_x = np.array([int(x) for x in sudoku]).reshape(9,9,1)
            X.append(np_solved_x)

    #zero centering X value
    np_X = np.array(X)
    np_X = np_X/9
    np_X -= 0.5
    np_y = np.array(y)

    return np_X, np_y


x = get_data()
