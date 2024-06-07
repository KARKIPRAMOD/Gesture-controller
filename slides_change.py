import cv2 as cv
import mediapipe as mp
import pyautogui

cam_index = 1
capture = cv.VideoCapture(cam_index)
if not capture.isOpened():
    print("Error: Could not open the camera")
    exit()

frame_width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
v_mid = frame_width // 2
frame_height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
h_mid = frame_height // 2

speaker_icon = (10,10)
arrow_icon = (10,10)
speaker_mode = False


text = f'camera {cam_index}'
font = cv.FONT_HERSHEY_SIMPLEX
position = (10, 50)
font_scale = 1
font_color = (0, 255, 0)
thickness = 2
line_type = cv.LINE_AA

myhands = mp.solutions.hands.Hands()
drawing = mp.solutions.drawing_utils

p_x8, p_y8 = 0, 0
p_x12, p_y12 = 0, 0
swipe_text = ""
volume_text = ""

while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break

    rgb_format = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = myhands.process(rgb_format)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark

            x8 = int(landmarks[8].x * frame.shape[1])
            y8 = int(landmarks[8].y * frame.shape[0])
            x4 = int(landmarks[4].x * frame.shape[1])
            y4 = int(landmarks[4].y * frame.shape[0])
            x12 = int(landmarks[12].x * frame.shape[1])
            y12 = int(landmarks[12].y * frame.shape[0])

            if p_x8 and p_y8  and p_x12  and p_y12 != 0:
                if p_x8 < v_mid and x8 > v_mid and p_x12 < v_mid and x12 > v_mid:
                    pyautogui.press('right')
                    swipe_text = "Swiped Right"
                    print(swipe_text)
                    p_x8 = p_x12 = 0
                elif p_x8 > v_mid and x8 < v_mid and p_x12 > v_mid and x12 < v_mid:
                    pyautogui.press('left')
                    swipe_text = "Swiped Left"
                    print(swipe_text)
                    p_x8 = p_x12 = 0

                if p_y8 > h_mid and y8 < h_mid and p_y12 > h_mid and y12 < h_mid:
                    pyautogui.press('up')
                    swipe_text = "Swiped Up"
                    print(swipe_text)
                    p_y8 = p_y12 = 0
                elif p_y8 < h_mid and y8 > h_mid and p_y12 < h_mid and y12 > h_mid:
                    pyautogui.press('down')
                    swipe_text = "Swiped Down"
                    print(swipe_text)
                    p_y8 = p_y12 = 0

            dist = ((x8 - x4)**2 + (y8 - y4)**2) ** 0.5
            if dist > 100: 
                pyautogui.press('volumeup')
                volume_text = "Volume Up"
            else:
                pyautogui.press('volumedown')
                volume_text = "Volume Down"

            p_x8, p_y8, p_x12, p_y12 = x8, y8, x12, y12

            cv.line(frame, (x4, y4), (x8, y8), (0, 255, 0), 5)
            cv.circle(frame, (x4, y4), 8, (0, 0, 255), 3)
            cv.circle(frame, (x8, y8), 8, (0, 255, 255), 3)
            cv.circle(frame, (x12, y12), 8, (255, 0, 0), 3)

    cv.line(frame, (v_mid, 0), (v_mid, frame.shape[0]), (0, 255, 0), 2)
    cv.line(frame, (0, h_mid), (frame.shape[1], h_mid), (0, 255, 0), 2)

    cv.putText(frame, text, position, font, font_scale, font_color, thickness, line_type)
    cv.putText(frame, swipe_text, (10, 100), font, font_scale, (255, 0, 0), thickness, line_type)
    cv.putText(frame, volume_text, (10, 150), font, font_scale, (255, 0, 0), thickness, line_type)
    cv.imshow('Camera', frame)


    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
