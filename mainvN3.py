import mediapipe as mp 
import cv2
import numpy as np
import uuid
import os
import math
import pyautogui
from config import *

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

def actualDistance(wristlm, fingerlm):
    length = math.sqrt((wristlm.x - fingerlm.x)**2 + (wristlm.y - fingerlm.y)**2)
    return math.sqrt(length**2 + (wristlm.z - fingerlm.z)**2)

def normalized(lankmark):
    x_px = min(math.floor(lankmark.x * img_width), img_width - 1)
    y_px = min(math.floor(lankmark.y * img_height), img_height - 1)
    return x_px, y_px

isMove = False
resultX = 0
resultY = 0

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        img_height, img_width, c = frame.shape

        frame = cv2.flip(frame, 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                if CAM_MODE:
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                    )
                for idx, landmark in enumerate(hand.landmark): 
                    if idx == 4:
                        wristlm = landmark
                    if idx == 12:
                        fingerlm = landmark
                    if idx == 8:
                        posX, posY = normalized(landmark)
                #print(actualDistance(wristlm, fingerlm))
                pointer = actualDistance(wristlm, fingerlm) > 0.065
                
                if pointer:
                    posX = round((posX / img_width) * SCREEN_WIDTH, 0)
                    posY = round((posY / img_height) * SCREEN_HEIGHT, 0)
                    if abs((posX+posY)-(resultX+resultY)) > 10:
                        resultX = posX
                        resultY = posY
                        
                    pyautogui.moveTo(resultX, resultY,_pause=False)
                    isMove = True
                elif isMove:
                    pyautogui.click()
                    print("click")
                    isMove = False     
        else:
            isMove = False       

        if CAM_MODE:
            cv2.imshow('Hand Tracking', image)       

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()



