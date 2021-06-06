from shapeExtractor import *

DIR = '4.jpg'

ex = Extractor(DIR)

sudoku = ex.get_digits()

print(type(sudoku))






"""


#cv2.imshow('1', image)
cv2.imshow('cropped', cropped)
cv2.imshow('4', main_board)
cv2.imwrite('res1.png', main_board)
cv2.waitKey()

"""
