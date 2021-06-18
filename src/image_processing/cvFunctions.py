import math

import cv2
import numpy as np
import imutils

def findBoards(img, area_length, inv = True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if inv:
        BINARY_MODE =  cv2.THRESH_BINARY_INV
    else:
        BINARY_MODE =  cv2.THRESH_BINARY

    thresh = cv2.threshold(gray, 100, 255, BINARY_MODE)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnt_sudoku = []
    for c in contours:
        if cv2.contourArea(c) > area_length:
            cnt_sudoku.append(c)

    boxes = []

    for c in cnt_sudoku:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        x = box[0][0]-box[2][0]
        y = box[0][1]-box[2][1]
        l = math.sqrt(x**2 + y**2)
        if not inv and l > 200:
            continue
        boxes.append(box)

    if len(boxes)>1:
        """
        This functionality is for fixing internal boards order.
        Some box starts counting from different point
        """

        box_center = []
        for b in boxes:
            # get global center of a box
            x = abs(b[0][0]-b[2][0])//2 + np.amin(b, axis=0)[0]
            y = abs(b[0][1]-b[2][1])//2 + np.amin(b, axis=0)[1]
            box_center.append([x, y])

        # sort by y, then each row by x
        sorted_y = sorted(box_center, key=lambda a: a[1])
        row1 = sorted_y[:3]
        row2 = sorted_y[3:6]
        row3 = sorted_y[6:]

        sorted_centers = sorted(row1, key=lambda a: a[0])
        for s in (sorted(row2, key=lambda a: a[0])):
            sorted_centers.append(s)
        for s in (sorted(row3, key=lambda a: a[0])):
            sorted_centers.append(s)

        # get proper indices for internal boxes
        indices = []

        for bc in box_center:
            index = sorted_centers.index(bc)
            indices.append(index)
        # sort by list of indices
        l = sorted(zip(boxes, indices), key = lambda a: a[1])

        box_buffer = []
        for cords, index in l:
            box_buffer.append(cords)
        boxes = box_buffer

    return boxes

def cropFromCords(image, cords):
    polygon = [[cords[0], cords[1], cords[2], cords[3]]]

    minX = image.shape[1]
    maxX = -1
    minY = image.shape[0]
    maxY = -1
    for point in polygon[0]:

        x = point[0]
        y = point[1]

        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y

    cropedImage = np.zeros_like(image)
    for y in range(0,image.shape[0]):
        for x in range(0, image.shape[1]):

            if x < minX or x > maxX or y < minY or y > maxY:
                continue

            if cv2.pointPolygonTest(np.asarray(polygon), (x, y), False) >= 0:
                cropedImage[y, x, 0] = image[y, x, 0]
                cropedImage[y, x, 1] = image[y, x, 1]
                cropedImage[y, x, 2] = image[y, x, 2]

    final = cropedImage[minY:maxY, minX:maxX]
    return final


def fixAngle(img, box):
    box_sorted = sorted(box, key=lambda a: a[1])
    a = box_sorted[1][1]-box_sorted[0][1]
    b = box_sorted[1][0]-box_sorted[0][0]

    rad = math.atan2(a, b)
    deg = 180 * rad / math.pi

    if b < 0:
        deg = deg + 180

    rotated = imutils.rotate(img, deg)

    h, w = rotated.shape[:2]
    crop_side = a // 2 + 3
    fixed = rotated[crop_side:h - crop_side, crop_side:w - crop_side]
    return fixed

def prepare_image(img):
    isNumber = False
    img = cv2.resize(img, (70, 70))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shape_threshold = 100.0

    for c in contours:
        if cv2.contourArea(c) > shape_threshold:
            isNumber = True
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.drawContours(img, [box], 0, (0, 0, 255), 1)

            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, pts=[box], color=(255, 255, 255))

            filtered_image = cv2.bitwise_and(thresh, mask)

            img = filtered_image

    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)[1]

    if isNumber:
        return img
    else:
        return np.full((70, 70, 3), 255, dtype=np.uint8)

def draw_sudoku(unsolved, solved):
    size = 400
    board = np.full((size, size, 3), 255, dtype=np.uint8)

    for i in range(10):
        if i % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        cv2.line(board, (i * size // 9, 0), (i * size // 9, size), (0, 0, 0), thickness)
        cv2.line(board, (0, i * size // 9), (size, i * size // 9), (0, 0, 0), thickness)

    cv2.line(board, (size, 0), (size, size), (0, 0, 0), 3)
    cv2.line(board, (0, size), (size, size), (0, 0, 0), 3)

    for i in range(9):
        for j in range(9):
            if unsolved[i][j] == solved[i][j]:
                COLOR = (0, 0, 0)
            else:
                COLOR = (64, 219, 17)

            cv2.putText(board, str(solved[i][j]), (j * size // 9 + 13, i * size // 9 + 33), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        COLOR, 2, cv2.LINE_AA)
    cv2.imshow('SUDOKU', board)
    cv2.waitKey()
