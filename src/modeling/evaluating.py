import numpy as np

def solve_batch(np_boards, np_solved_boards, model):
    """Solve batch of sudoku boards, trying to guess whole board in one prediction.

    Arguments:
        np_boards {NumPy array} -- unsolved sudoku boards with shape (x,9,9,1) and values in a range <-0.5, 0.5>.
            To get this range you should divide standard boards values by 9 and subtract 0.5.
        np_solved_boards {NumPy array} -- solved sudoku boards with shape (x,9,9,1) and values in a range <0, 8>.
            To get this range you should substract 1 from standard boards values
        model {Sequential} -- trained Keras model, which should be used by this function

    Returns:
        [float] -- solving accuracy (range <0.0, 1.0>)
    """
    np_results = np.empty(np_boards.shape[0],dtype=np.bool_)
    for i in np.ndindex(np_boards.shape[:1]):
        predictions = model.predict(np_boards[i].reshape(1,9,9,1))[0]
        solved = np.argmax(predictions, axis=1).reshape((9,9)) +1
        np_results[i] = compare_sudoku(solved, (np_solved_boards[i]+1).reshape(9,9))
        print(f"Solving sudoku number: {i}")
    correct_boards = np_results.sum()
    acc = correct_boards/np_boards.shape[0]
    return acc

def solve_human_batch(np_boards, np_solved_boards, model):
    """Solve batch of sudoku boards, using a more human approach. This means guessing digits one by one (only digit with the highest probability value)

    Arguments:
        np_boards {NumPy array} -- unsolved sudoku boards with shape (x,9,9,1) and values in a range <-0.5, 0.5>.
            To get this range you should divide standard boards values by 9 and subtract 0.5.
        np_solved_boards {NumPy array} -- solved sudoku boards with shape (x,9,9,1) and values in a range <0, 8>.
            To get this range you should subtract 1 from standard boards values
        model {Sequential} -- trained Keras model, which should be used by this function

    Returns:
        [float] -- solving accuracy (range <0.0, 1.0>)
    """
    np_results = np.empty(np_boards.shape[0],dtype=np.bool_)
    for i in np.ndindex(np_boards.shape[:1]):
        solved = solve_human_approach(np_boards[i], model)
        np_results[i] = compare_sudoku(solved, (np_solved_boards[i]+1).reshape(9,9))
        print(f"Solving sudoku number: {i}")
    correct_boards = np_results.sum()
    acc = correct_boards/np_boards.shape[0]
    return acc

def solve_human_approach (np_sample_board, model): 
    """Solve single sudoku boards using a more human approach. This means guessing digits one by one (only digit with the highest probability value)

    Arguments:
        np_sample_board {NumPy array} -- unsolved sudoku board with shape (9,9,1) and values in a range <-0.5, 0.5>.
            To get this range you should divide standard boards values by 9 and subtract 0.5.
         model {Sequential} -- trained Keras model, which should be used by this function

    Returns:
        [NumPy array] -- solved sudoku board with valid values (range <1,9>)
    """
    np_board = np.copy(np_sample_board)

    while(1):
        np_board_4d = np_board.reshape((1,9,9,1))
        predictions = model.predict(np_board_4d)[0]
        predictions_int = np.argmax(predictions, axis=1).reshape((9,9))+1           #change range of digits from <0,8> to <1,9>
        propabilities = np.around(np.max(predictions, axis=1).reshape((9,9)), 2) 
                        
        #get position with the highest probability
        np_board = detransform(np_board).reshape((9,9))
        zeros = (np_board == 0)
        if (zeros.sum() == 0):
            break
        blanks_indices = np.where(zeros)
        blanks_indices = np.array([(i,j) for i,j in zip(blanks_indices[0], blanks_indices[1])])
        position_to_fill = blanks_indices[propabilities[zeros].argmax()]
        #fill position with the highest probability
        value_to_fill = predictions_int[position_to_fill[0], position_to_fill[1]]
        
        np_board[position_to_fill[0], position_to_fill[1]] = value_to_fill
        np_board = transform(np_board)

    return np_board

    
def compare_sudoku (np_sudoku1, np_sudoku2):
    """Comparing two sudoku boards with identical shapes and range of values

    Arguments:
        np_sudoku1 {NumPy array} -- first board to compare
        np_sudoku2 {NumPy array} -- second board to compare

    Returns:
        [int] -- 1 if boards are identical, 0 otherwise
    """
    #True/False array
    comparision = np_sudoku1 == np_sudoku2

    return comparision.all()

def transform(np_a):
    """Transforming sudoku board from range <0,9>, to <-0.5,0.5>.

    Arguments:
        np_a {NumPy array} -- sudoku board to transform

    Returns:
        [NumPY array] -- transformed sudoku board
    """
    
    return (np_a/9)-0.5

def detransform(np_a):
    """Transforming sudoku board from range <-0.5,0.5>, to <0,9>

    Arguments:
        np_a {NumPy array} -- sudoku board to transform

    Returns:
        [NumPY array] -- transformed sudoku board
    """
    return (np_a+0.5)*9