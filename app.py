import cv2
from mss import mss
import numpy as np
import pyautogui
import time
import datetime


def get_img_score(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_green = hsv_img[:,:,1]
    return cv2.mean(img_green)[0]

# Define the coordinates and size of the region of interest (ROI)
roi = {'left': 843, 'top': 634, 'width': 100, 'height': 100}

# Set the cooldown duration (in seconds)
cooldown_duration = 3

# Set the time of the last click
last_click_time = time.time()

while True:
    # Capture the region of interest from the screen
    with mss() as sct:
        sct_img = sct.grab(roi)
        # Convert to a numpy array and show in a window using cv2
        img = np.array(sct_img)
    
    score = get_img_score(img)

    # Check if the cooldown has passed
    if time.time() - last_click_time >= cooldown_duration:
        cv2.putText(img, "Score: {:.2f}".format(score), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if (score > 45 or score < 20):
            pyautogui.click()
            last_click_time = time.time()
            # Print a message to indicate that a click was performed
            print("Click performed at {}".format(time.strftime("%H:%M:%S")))
    else:
        cv2.putText(img, "Score: {:.2f}".format(score), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)



    cv2.imshow('ROI', img)

    key = cv2.waitKey(1)
    # Exit on 'q' keypress
    if key == ord('q'):
        break

    # Capture on 'c'
    if key == ord('c'):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        cv2.imwrite(f'{timestamp}.jpg', img)
        print(f'Frame captured at {timestamp}.jpg')

# Clean up
cv2.destroyAllWindows()
