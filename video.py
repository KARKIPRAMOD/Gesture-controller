#READING VIDEOS
import cv2 as cv
cam_index = 0
capture  = cv.VideoCapture(cam_index)

if not capture.isOpened():
    print("Error: Could not open the camera")
    exit()

text= f'camera {cam_index}'
font = cv.FONT_HERSHEY_SIMPLEX
position =(10,50)
font_scale = 1
font_color = (0,255,0)
thickness = 2
line_type = cv.LINE_AA

#READ AND DISPLAY THE IMAGE
while True:
    isTrue, frame = capture.read()
    cv.putText(frame, text, position, font, font_scale, font_color, thickness,line_type)
    cv.imshow('Camera', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()