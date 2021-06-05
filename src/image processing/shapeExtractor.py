import pytesseract
from cvFunctions import *


class Extractor:
    def __init__(self, dir):
        self.image = self.get_sudoku_image(dir)
        self.sudoku_squares = []
        self.digits = []

    def get_digits(self):
        self.find_sudoku()
        self.get_sudoku_squares()
        self.get_single_digit()
        return self.digits

    def get_sudoku_image(self, img_dir):
        image = cv2.imread(img_dir)
        image = cv2.resize(image, (600, 600))
        cv2.imshow('image', image)
        return image

    def find_sudoku(self):
        # get cords for main sudoku board
        mb_cords = findBoards(self.image, 7e4)

        for c in mb_cords:
            cropped = cropFromCords(self.image, c)
            self.main_board = fixAngle(cropped, c)

    def get_sudoku_squares(self):
        # get cords for internal boards
        ib_cords = findBoards(self.main_board, 1e3, False)
        print(len(ib_cords))

        for i, c in enumerate(ib_cords):
            cropped = cropFromCords(self.main_board, c)
            fixed = fixAngle(cropped, c)
            self.sudoku_squares.append(fixed)
            # cv2.imwrite(f'pieces/{i}.png', fixed)

    def get_single_digit(self):
        for square in self.sudoku_squares:
            h, w = square.shape[:2]

            digits_in_square = []

            for i in range(3):
                for j in range(3):
                    slice = square[i * h // 3:(i + 1) * h // 3, j * w // 3:(j + 1) * w // 3]

                    self.extract_digit(slice)
                    digits_in_square.append(slice)
            self.digits.append(digits_in_square)

    def extract_digit(self, img):
        img = prepare_image(img)
        cv2.imshow('extract', img)

        # numbers only
        config_1 = '--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'
        # numbers, letters and other characters
        config_2 = '--psm 10 --oem 3 tessedit_char_whitelist=123456789'

        ocr = pytesseract.image_to_string(img, config=config_1)
        for o in ocr:
            if o.isnumeric():
                digit = int(o)
                return digit

        ocr = pytesseract.image_to_string(img, config=config_2)
        for o in ocr:
            if o == 'Q':
                digit = 9
            else:
                digit = 0
            return digit



"""
ex = Extractor()
img = cv2.imread('pieces/d/7.png')
digit = ex.extract_digit(img)
print(digit)
cv2.waitKey()
"""