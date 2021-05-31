from cvFunctions import *

image = cv2.imread('4.jpg')
image = cv2.resize(image, (600, 600))

#get cords for main sudoku board
mb_cords = findBoards(image, 7e4)

for c in mb_cords:
    cropped = cropFromCords(image, c)
    main_board = fixAngle(cropped, c)

#get cords for interior boards
ib_cords = findBoards(main_board, 1000, False)

for i, c in enumerate(ib_cords):
    cropped2 = cropFromCords(main_board, c)
    #fixed = fixAngle(cropped, c)
    #print(i)
    cv2.imwrite(f'pieces/{i}.png', cropped2)


cv2.imshow('1', image)
cv2.imshow('4', main_board)
#cv2.imwrite('r4.png', main_board)
cv2.waitKey()


