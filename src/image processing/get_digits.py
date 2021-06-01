import cv2

from cvFunctions import *

image = cv2.imread('3.jpg')
image = cv2.resize(image, (600, 600))
cv2.imshow('image', image)


#get cords for main sudoku board
mb_cords = findBoards(image, 7e4)

for c in mb_cords:
    cropped = cropFromCords(image, c)
    main_board = fixAngle(cropped, c)

#get cords for internal boards
ib_cords = findBoards(main_board, 1e3, False)
print(len(ib_cords))


for i, c in enumerate(ib_cords):
    cropped = cropFromCords(main_board, c)
    fixed = fixAngle(cropped, c)
    cv2.imwrite(f'pieces/{i}.png', fixed)


#cv2.imshow('1', image)
cv2.imshow('cropped', cropped)
cv2.imshow('4', main_board)
cv2.imwrite('res1.png', main_board)
cv2.waitKey()


