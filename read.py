import cv2 as cv

img = cv.imread('photos/1.jpg')
cv.imshow('picture',img)
cv.waitKey(0)