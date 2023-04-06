import cv2
from mss import mss
import numpy as np
import pyautogui
import time

# Define the coordinates and size of the region of interest (ROI)
roi = {'left': 843, 'top': 634, 'width': 100, 'height': 100}

ref_img = cv2.imread('reel.jpeg')
hsv_ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2HSV)
ref_green = hsv_ref_img[:,:,1]
mean_green_ref = cv2.mean(ref_green)[0]

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

    if time.time() - last_click_time >= cooldown_duration:
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_green = hsv_img[:,:,1]
        mean_green_img = cv2.mean(img_green)[0]

        score = mean_green_img/mean_green_ref
        # print("score: {}", score)

        if (score > 0.6 and score < 1.0):
            # Check if the cooldown has passed
                pyautogui.click()
                last_click_time = time.time()

                # Print a message to indicate that a click was performed
                print("Click performed at {}".format(time.strftime("%H:%M:%S")))
            # else:
                # Print a message to indicate that a click was skipped due to cooldown
                # print("Click skipped due to cooldown")

    cv2.imshow('ROI', img)

    # Exit on 'q' keypress
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
