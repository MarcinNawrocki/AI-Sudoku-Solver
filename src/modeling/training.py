import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Reshape, BatchNormalization, Activation, Input, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.backend import set_value


def get_model():
    """Return a neural network model created using Keras to solve a sudoku 

    Returns:
        [Sequential] -- compiled Keras model to solve sudoku
    """
    input_shape = (9, 9, 1)
    model = Sequential()

    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu',
              padding='same', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(1, 1),
              activation='relu', padding='same'))

    model.add(Flatten())
    model.add(Dense(81*9))
    model.add(Reshape((-1, 9)))
    model.add(Activation('softmax'))

    adam = Adam(learning_rate=0.001)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=adam, metrics=['accuracy'])

    return model


def load_model(approach):
    """Load one of the pretrained model to solve a sudoku board

    Arguments:
        approach {int} -- specifies for which approach model should be loaded (possible values: 1 or 2)

    Returns:
        [Sequential] -- a trained Keras model to solve sudoku
    """
    if approach == 1:
        filename = "./model/CNN.hp5"
    elif approach == 2:
        filename = "./model/CNN.hp5"

    model = tf.keras.models.load_model(filename, compile=False)
    return model


def training_first_approach(model, dataset, batch_size=128):
    """Execute training with Sudoku Boards using first approach settings

    Arguments:
        model {Sequential} -- compiled Keras model to train on a sudoku boards
        dataset {tuple of NumPy arrays} -- tuple containing X_train, X_test, y_train, y_test as NumPy arrays

    Keyword Arguments:
        batch_size {int} -- batch size using during learning (default: {128})

    Returns:
        [Sequential] -- trained Keras model using the first approach
    """
    X_train, X_test, y_train, y_test = dataset
    early_stop = EarlyStopping(
        monitor='val_loss', patience=2, restore_best_weights=True)
    with tf.device('/GPU:0'):
        model.fit(X_train, y_train, epochs=5, batch_size=batch_size,
                  validation_data=[X_test, y_test], callbacks=[early_stop])

    return model


def training_second_approach(model, dataset, epochs, digits, batch_size=32):
    """Execute training with Sudoku Boards using second approach settings

    Arguments:
        model {Sequential} -- compiled Keras model to train on a sudoku boards
        dataset {tuple of NumPy arrays} -- tuple containing X_train, X_test, y_train, y_test as NumPy arrays
        epochs {list of ints} -- specifies how many epochs should model learn during each stage 
        digits {list of ints} -- specifies how many digits should be removed from sudoku boards (training dataset) during each stage 

    Keyword Arguments:
       batch_size {int} -- batch size using during learning (default: {128})

    Returns:
        [Sequential] -- trained Keras model using the second approach
    """
    # sprawdzic czy te same długości
    X_train, X_test, y_train, y_test = dataset
    early_stop = EarlyStopping(
        monitor='val_loss', patience=1, restore_best_weights=True)
    i = 1
    for _epochs, _delete in zip(epochs, digits):
        print(f'Pass stage number {i}')
        i += 1
        with tf.device('/GPU:0'):
            model.fit(delete_digits(X_train, _delete), y_train,
                      validation_data=(delete_digits(X_test, _delete), y_test),
                      epochs=_epochs, batch_size=16, callbacks=[early_stop])
    return model


def delete_digits(np_Y, digits_to_delete=1):
    """Function deletes a specified number of digits from each sudoku board in passed batch.

    Arguments:
        np_Y {NumPy array} -- batch of solved sudoku boards with shape (x,9,9,1) and values in a range <-0.5, 0.5>.
            To get this range you should divide standard boards values by 9 and subtract 0.5.

    Keyword Arguments:
        digits_to_delete {int} -- number of digits to delete (substitute as value representing NULL)  (default: {1})

    Returns:
        [NumPy array] -- a batch of sudoku boards with the deleted specified number of digits
    """
    np_boards = np_Y.copy()
    for np_board in np_boards:
        np_board.flat[np.random.randint(0, 81, digits_to_delete)] = - 0.5
    return np_boards
