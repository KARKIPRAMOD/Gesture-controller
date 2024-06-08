import cv2 as cv
import mediapipe as mp
import pyautogui
import time

cam_index = 1  # TO ACCESS THE CAMERA
capture = cv.VideoCapture(cam_index)  # CAPTURES THE FRAMES FROM THE CAM
if not capture.isOpened():
    print("Error: Could not open the camera")
    exit()

frame_width = int(capture.get(cv.CAP_PROP_FRAME_WIDTH))
v_mid = frame_width // 2
frame_height = int(capture.get(cv.CAP_PROP_FRAME_HEIGHT))
h_mid = frame_height // 2

#################### CREATING A MODE VOLUME OR ARROW ####################
speaker_icon_position = (600, 50)  # Position for the speaker icon
speaker_icon_size = 30
speaker_mode = False
mode = ""  # Initialize mode variable

##### TIMER VARIABLES #####
timer_started = False
timer_start_time = 0
activation_duration = 3  #Takes 3 seconds to activate volume mode
volume_mode_duration = 5  #Stays active for only 5 seconds

#################### TEXT FUNCTIONS ####################
text = f'camera {cam_index}'
font = cv.FONT_HERSHEY_SIMPLEX
position = (10, 50)
font_scale = 1
font_color = (46, 204, 113)
thickness = 2
line_type = cv.LINE_AA

#################### FUNCTIONS TO DETECT HANDS AND DRAW KEYPOINTS ####################
myhands = mp.solutions.hands.Hands()
drawing = mp.solutions.drawing_utils

#################### VARIABLES TO STORE PREVIOUS COORDINATES OF KEYPOINTS ####################
p_x8, p_y8 = 0, 0
p_x12, p_y12 = 0, 0
swipe_text = ""
volume_text = ""

#################### FUNCTION TO CHANGE VOLUMES BASED ON THE FINGER KEYPOINTS ####################
def volume_control(x8, x4, y8, y4):
    global volume_text  # Use global to modify the variable outside the function
    dist = ((x8 - x4) ** 2 + (y8 - y4) ** 2) ** 0.5
    if dist > 100:
        pyautogui.press('volumeup')
        volume_text = "Volume Up"
    else:
        pyautogui.press('volumedown')
        volume_text = "Volume Down"

#################### THIS LOOPS CONTINUOUSLY WORK UNTIL THE CAMERA IS SHUT OFF OR USER CLOSES THE APPLICATION ####################
while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break

    rgb_format = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = myhands.process(rgb_format)
    hands = output.multi_hand_landmarks

    #################### IF HAND IS DETECTED THEN IT FINDS THE LANDMARK (coordinates of the keypoints) ####################
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

           # dist_to_icon = ((x8 - speaker_icon_position[0]) ** 2 + (y8 - speaker_icon_position[1]) ** 2) ** 0.5
            dist_to_icon =  ((x8 - speaker_icon_position[0]) ** 2 + (y8 -speaker_icon_position[1]) ** 2) ** 0.5
            if dist_to_icon <= speaker_icon_size:
                if timer_start_time == 0:
                    timer_start_time = time.time()
                    
                elif time.time() - timer_start_time >= activation_duration:
                    speaker_mode = True
                    mode = "MODE: VOLUME Control"
                    volume_mode_start_time = time.time()
            else:
                timer_start_time = 0

            if speaker_mode is False:       ########## CHECKS WHETHER THE SPEAKER MOD IS ON OR OFF ##########
                mode = "MODE: ARROW Keys"
                if p_x8 and p_y8 and p_x12 and p_y12 != 0:
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

                cv.putText(frame, swipe_text, (10, 140), font, font_scale, (255, 255, 0), thickness, line_type)  # Orange text
                cv.circle(frame, speaker_icon_position, speaker_icon_size, (0, 255, 0), 3)  # Green circle
            else:
                mode = "MODE: VOLUME Control"
                volume_control(x8, x4, y8, y4)
                if time.time() - volume_mode_start_time >= volume_mode_duration:
                    speaker_mode = False  # Switch back to arrow mode after 3 seconds
                cv.putText(frame, volume_text, (10, 170), font, font_scale, (255, 255, 0), thickness, line_type)  # Orange text
            p_x8, p_y8, p_x12, p_y12 = x8, y8, x12, y12

            cv.line(frame, (x4, y4), (x8, y8), (0, 255, 0), 5)
            cv.circle(frame, (x4, y4), 8, (0, 0, 255), 3)
            cv.circle(frame, (x8, y8), 8, (0, 255, 255), 3)
            cv.circle(frame, (x12, y12), 8, (255, 0, 0), 3)
    cv.putText(frame, text, position, font, font_scale, (255, 255, 0), thickness, line_type)  # Yellow text
    cv.line(frame, (v_mid, 0), (v_mid, frame.shape[0]), (0, 0, 0), 2)  # Cyan line
    cv.line(frame, (0, h_mid), (frame.shape[1], h_mid), (0, 0, 0), 2)  # Magenta line
    cv.putText(frame, mode, (10, 100), font, font_scale, (0, 255, 255), thickness, line_type)  # Cyan text

    cv.imshow('Camera', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
