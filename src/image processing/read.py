import cv2
import numpy as np
import imutils


img = cv2.imread('shapes/1/1_0.png')
img = cv2.resize(img, (70, 70))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
"""
cnt = []
for c in contours:
    cnt.append(cv2.contourArea(c))


if cnt and max(cnt) > 105.0:
    i = cnt.index(max(cnt))
    digit_contour = contours[i]

img2 = cv2.imread('4_5.png')

gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
thresh2 = cv2.threshold(gray2, 100, 255, cv2.THRESH_BINARY_INV)[1]
thresh2 = cv2.threshold(gray2, 127, 255,0)[1]
contours,hierarchy = cv2.findContours(thresh,2,1)

print(type(digit_contour))
ret = cv2.matchShapes(digit_contour,contours,1,0.0)
print(ret)

"""





for c in contours:
    print(cv2.contourArea(c))
    if cv2.contourArea(c) > 100.0:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 1)

        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, pts=[box], color=(255,255,255))

        filtered_image = cv2.bitwise_and(thresh, mask)



#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
# Create an empty output image to hold values
#thin = np.zeros(img.shape[:2], dtype='uint8')

# Loop until erosion leads to an empty set
    # Erosion
#erode = cv2.erode(filtered_image, kernel)
# Opening on eroded image
#opening = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)
# Subtract these two
#subset = erode - opening
# Union of all previous sets
#thin = cv2.bitwise_or(subset, thin)
# Set the eroded image for next iteration

#img2 = cv2.imread('3_2.png')
#mg3 = cv2.imread('8_4.png')
#img2 = cv2.resize(img2, (70, 70))
#img3 = cv2.resize(img3, (70, 70))

#gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#gray2 = cv2.threshold(gray2, 100, 255, cv2.THRESH_BINARY)[1]

#gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
#gray3 = cv2.threshold(gray3, 100, 255, cv2.THRESH_BINARY)[1]

#ret = cv2.matchShapes(filtered_image,gray2,1,0.0)
#ret2 = cv2.matchShapes(filtered_image,gray3,1,0.0)

#print(ret)
#print(ret2)
cv2.imshow('s',filtered_image)
#cv2.imshow('g', gray3)
#cv2.imshow('ss', gray2)


cv2.waitKey()
