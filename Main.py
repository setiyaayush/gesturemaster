import cv2
import time
import math
import numpy as np
import HandTrackingModule as htm
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Camera settings
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# Hand detector initialization
detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

# Audio control setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

minVol = -63
maxVol = volRange[1]

# Initialization variables
hmin = 50
hmax = 200
volBar = 400
volPer = 0
vol = 0
color = (0, 215, 255)

tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0

pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()

# Function to display mode on the screen with enhanced design
def putText(img, text, loc=(250, 450), color=(0, 255, 255), font_scale=1.5, thickness=3):
    cv2.putText(img, str(text), loc, cv2.FONT_HERSHEY_COMPLEX, font_scale, color, thickness)

# Function to add a stylish rectangle
def drawRect(img, top_left, bottom_right, color, thickness=3, rounded=False):
    if rounded:
        cv2.rectangle(img, top_left, bottom_right, color, thickness, lineType=cv2.LINE_AA)
    else:
        cv2.rectangle(img, top_left, bottom_right, color, thickness)

# Main loop
while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame. Check camera connection.")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    fingers = []

    if len(lmList) != 0:
        # Thumb
        fingers.append(1 if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1] else 0)
        # Other fingers
        for id in range(1, 5):
            fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

        # Determine mode
        if fingers == [0, 0, 0, 0, 0] and active == 0:
            mode = 'N'
        elif fingers in ([0, 1, 0, 0, 0], [0, 1, 1, 0, 0]) and active == 0:
            mode = 'Scroll'
            active = 1
        elif fingers == [1, 1, 0, 0, 0] and active == 0:
            mode = 'Volume'
            active = 1
        elif fingers == [1, 1, 1, 1, 1] and active == 0:
            mode = 'Cursor'
            active = 1

    # Scroll mode
    if mode == 'Scroll':
        putText(img, mode, loc=(250, 50))
        if len(lmList) != 0:
            if fingers == [0, 1, 0, 0, 0]:
                putText(img, 'Scroll Up', loc=(200, 455), color=(0, 255, 0))
                pyautogui.scroll(300)
            elif fingers == [0, 1, 1, 0, 0]:
                putText(img, 'Scroll Down', loc=(200, 455), color=(0, 0, 255))
                pyautogui.scroll(-300)
            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'

    # Volume mode
    if mode == 'Volume':
        putText(img, mode, loc=(250, 50))
        if len(lmList) != 0:
            if fingers[-1] == 1:
                active = 0
                mode = 'N'
            else:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), color, 3)
                cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)

                length = math.hypot(x2 - x1, y2 - y1)

                vol = np.interp(length, [hmin, hmax], [minVol, maxVol])
                volBar = np.interp(vol, [minVol, maxVol], [400, 150])
                volPer = np.interp(vol, [minVol, maxVol], [0, 100])

                volume.SetMasterVolumeLevel(vol, None)

                if length < 50:
                    cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)

                # Stylish volume bar
                drawRect(img, (30, 150), (55, 400), (209, 206, 0), 3)
                drawRect(img, (30, int(volBar)), (55, 400), (215, 255, 127), -1, rounded=True)
                cv2.putText(img, f'{int(volPer)}%', (25, 430), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)

    # Cursor mode
    if mode == 'Cursor':
        putText(img, mode, loc=(250, 50))
        if fingers[1:] == [0, 0, 0, 0]:
            active = 0
            mode = 'N'
        else:
            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]
                X = int(np.interp(x1, [110, 620], [0, screen_width - 1]))
                Y = int(np.interp(y1, [20, 350], [0, screen_height - 1]))
                pyautogui.moveTo(X, Y)
                if fingers[0] == 0:
                    pyautogui.click()

    # Frame rate display
    cTime = time.time()
    fps = 1 / ((cTime + 0.01) - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (480, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

    # Display final image
    cv2.imshow('Hand LiveFeed', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
