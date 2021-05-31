import cv2
import numpy as np
import math
import imutils

def findBoards(image, area_length, inv = True):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if inv:
        thresh = cv2.threshold(gray,100,255, cv2.THRESH_BINARY_INV)[1]
    else:
        thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #czarna plansza
    black_shape = np.zeros(image.shape)

    cnt_sudoku = []
    #wyodrebnij kontury > od zadanych 7e4 dla 600x600
    for c in contours:
        if cv2.contourArea(c) > area_length:
            cnt_sudoku.append(c)

    #draw green contours on black image
    imcnt = cv2.drawContours(black_shape, cnt_sudoku, -1, (0,255,0), 1)

    boxes = []
    #red rectangle box based on detected contour
    for c in cnt_sudoku:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        boxes.append(box)

    print(f"{box}")
    print(box[0], box[1])

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
    a = box[0][1] - box[1][1]
    b = box[0][0] - box[1][0]
    rad = math.atan2(a, b)
    deg = 180 * rad / math.pi

    rotated = imutils.rotate(img, deg)

    h, w = rotated.shape[:2]
    crop_side = a // 2 + 3

    fixed = rotated[crop_side:h - crop_side, crop_side:w - crop_side]
    if deg > 1:
        return fixed
    else:
        return img
