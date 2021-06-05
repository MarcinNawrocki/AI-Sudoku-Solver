import cv2


image = cv2.cvtColor(cv2.imread('pieces/6.png'), cv2.COLOR_BGR2RGB)

h, w = image.shape[:2]

digits_img = []

k = 0

for i in range(3):
    for j in range(3):
        slice = image[i * h//3:(i+1) * h//3, j * w//3:(j+1) * w//3]
        cv2.imwrite(f'pieces/d/{k}.png', slice)
        #digits_img.append(slice)
        k += 1


cv2.imshow('1', image)
cv2.waitKey()


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
