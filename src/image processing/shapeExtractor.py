import cv2
import pytesseract
from cvFunctions import *


class Extractor:
    def __init__(self, dir, debug=False):
        self.debug = self.isDebug(debug)
        self.image = self.get_sudoku_image(dir)
        self.sudoku_squares = []
        self.digits = []

    def isDebug(self, debug):
        if debug:
            print('[INFO] Debug mode on. Check digits')
        return debug

    def get_digits(self):
        print('[INFO] Extracting digits...')
        self.find_sudoku()
        self.get_sudoku_squares()
        self.get_single_digit()
        return self.digits

    def get_sudoku_image(self, img_dir):
        image = cv2.imread(img_dir)
        image = cv2.resize(image, (600, 600))
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

        for c in ib_cords:
            cropped = cropFromCords(self.main_board, c)
            fixed = fixAngle(cropped, c)
            self.sudoku_squares.append(fixed)

    def get_single_digit(self):
        k = 0
        for square in self.sudoku_squares:
            h, w = square.shape[:2]

            digits_in_square = []

            for i in range(3):
                for j in range(3):
                    slice = square[i * h // 3:(i + 1) * h // 3, j * w // 3:(j + 1) * w // 3]
                    prepared_slice = prepare_image(slice)
                    extracted_digit = self.extract_digit(prepared_slice)
                    if self.debug:
                        cv2.imshow('square', square)
                        cv2.imshow('digit', prepared_slice)
                        print(f'Extracted digit: {extracted_digit}')
                        print('[INFO] Press any key to continue...')
                        cv2.waitKey()
                    digits_in_square.append(extracted_digit)
            self.digits.append(digits_in_square)

    def extract_digit(self, img):
        # numbers only
        config_1 = '--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'
        # numbers, letters and other characters
        config_2 = '--psm 10 --oem 3 tessedit_char_whitelist=123456789'

        ocr = pytesseract.image_to_string(img, config=config_1)
        if self.debug:
            print(f'OCR1: {ocr}')

        for o in ocr:
            if o.isnumeric():
                digit = int(o)
                return digit

        ocr = pytesseract.image_to_string(img, config=config_2)
        if self.debug:
            print(f'OCR2: {ocr}')

        for o in ocr:
            if o.isnumeric():
                digit = int(o)
            elif o == 'Q': #in many cases ocr recognizes 9 as Q
                digit = 9
            else:
                digit = 0
            return digit

DIR = '6.jpg' #3.jpg wszystko rozpoznal

ex = Extractor(DIR, True)

sudoku = ex.get_digits()     

cv2. waitKey()
