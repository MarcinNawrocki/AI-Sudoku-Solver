import cv2
import numpy as np
import pytesseract

from cvFunctions import findBoards, cropFromCords, fixAngle, prepare_image


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
        self.get_single_digits()
        self.custom_sort()
        return self.digits

    def get_sudoku_image(self, img_dir):
        image = cv2.imread(img_dir)
        image = cv2.resize(image, (600, 600))
        return image

    def find_sudoku(self):
        """
        Finds coordinates for main board.
        """
        mb_cords = findBoards(self.image, 7e4)

        for c in mb_cords:
            cropped = cropFromCords(self.image, c)
            self.main_board = fixAngle(cropped, c)

    def get_sudoku_squares(self):
        """
        Finds coordinates of internal squares.
        """
        ib_cords = findBoards(self.main_board, 1e3, False)

        for c in ib_cords:
            cropped = cropFromCords(self.main_board, c)
            fixed = fixAngle(cropped, c)
            self.sudoku_squares.append(fixed)

    def get_single_digits(self):
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
        """
        OCR function uses two configs. Both recognize digits, but config 2 can also find
        letters. Thanks to it, ocr works more precisely.
        Also, in many cases ocr recognizes '9' as 'Q'

        """
        config_1 = '--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'
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
            elif o == 'Q':
                digit = 9
            else:
                digit = 0
            return digit

    def custom_sort(self):
        """
        Function sorting sudoku array into format acceptable by tensorflow model: rows x cols
        Initially every row was represented by each value of single sudoku square
        """
        sudoku = np.asarray(self.digits)
        temporary_list = []

        for s in sudoku:
            s = s.reshape(3, 3)
            temporary_list.append(s)

        sudoku = np.asarray(temporary_list)
        sudoku = np.concatenate(sudoku, axis=1)
        sudoku = sudoku.reshape(9, -1)

        order = [0, 3, 6, 1, 4, 7, 2, 5, 8]

        self.digits = sudoku[order]
