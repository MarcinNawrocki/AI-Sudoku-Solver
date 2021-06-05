import glob
import cv2
import pytesseract
from cvFunctions import prepare_image


class Extractor:
    def __init__(self):
        self.dataset = []
        self.load_shapes()

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

    def load_shapes(self):
        cats = list(range(1, 10))
        for c in cats:
            ds_dir = glob.glob(f'shapes/{c}/*')
            images = []
            for d in ds_dir:
                img = cv2.imread(d)
                img = prepare_image(img)
                digit = self.extract_digit(img)
                cv2.imshow(f'{c}', img)
                print(digit)
                cv2.waitKey()
                images.append(img)
            self.dataset.append(images)




ex = Extractor()
img = cv2.imread('pieces/d/7.png')
digit = ex.extract_digit(img)
print(digit)
cv2.waitKey()
