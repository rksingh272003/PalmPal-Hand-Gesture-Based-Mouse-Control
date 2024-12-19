import cv2
import mediapipe as mp
import pyautogui
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)
prev_x, prev_y = 0, 0
smoothening = 7

def is_finger_raised(tip, base):
    return tip.y < base.y  

def is_thumb_raised(tip, base):
    return tip.x < base.x  
while True:
    
    success, img = cap.read()
    if not success:
        continue

  
    img = cv2.flip(img, 1)

  
    frame_height, frame_width, _ = img.shape

   
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
           
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
         
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]

            little_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            little_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
 
            x = int(index_finger_tip.x * frame_width)
            y = int(index_finger_tip.y * frame_height)

            screen_x = np.interp(x, (0, frame_width), (0, screen_width))
            screen_y = np.interp(y, (0, frame_height), (0, screen_height))

            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            pyautogui.moveTo(curr_x, curr_y)

          
            prev_x, prev_y = curr_x, curr_y

          
            if is_finger_raised(index_finger_tip, index_finger_base) and \
               is_finger_raised(middle_finger_tip, middle_finger_base) and \
               not is_finger_raised(ring_finger_tip, ring_finger_base):
                pyautogui.click()
                print("Left Click")
                pyautogui.sleep(0.2)    
            elif is_finger_raised(index_finger_tip, index_finger_base) and \
                 is_finger_raised(middle_finger_tip, middle_finger_base) and \
                 is_finger_raised(ring_finger_tip, ring_finger_base) and \
                 not is_finger_raised(little_finger_tip, little_finger_base):
                pyautogui.click(button='right')
                print("Right Click")
                pyautogui.sleep(0.2)  
            elif is_finger_raised(index_finger_tip, index_finger_base) and \
                 is_finger_raised(middle_finger_tip, middle_finger_base) and \
                 is_finger_raised(ring_finger_tip, ring_finger_base) and \
                 is_finger_raised(little_finger_tip, little_finger_base) and \
                 not is_thumb_raised(thumb_tip, thumb_base):
                pyautogui.scroll(25)
                print("Scroll Up")
                pyautogui.sleep(0.2)  
            elif is_finger_raised(index_finger_tip, index_finger_base) and \
                 is_finger_raised(middle_finger_tip, middle_finger_base) and \
                 is_finger_raised(ring_finger_tip, ring_finger_base) and \
                 is_finger_raised(little_finger_tip, little_finger_base) and \
                 is_thumb_raised(thumb_tip, thumb_base):
                pyautogui.scroll(-25)
                print("Scroll Down")
                pyautogui.sleep(0.2) 

  
    cv2.imshow("Hand Tracking", img)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
