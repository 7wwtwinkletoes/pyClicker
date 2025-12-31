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

def is_activated(score, target, tolerance):
    return abs(score - target) <= tolerance

# Function to get current mouse position
def get_mouse_position():
    x, y = pyautogui.position()
    return x, y

# Define the coordinates and size of the region of interest (ROI)
print("\nMove your mouse to where you want to capture and press 'p' to set position and start clicking")
roi = {'left': 843, 'top': 634, 'width': 140, 'height': 140}  # default values
clicking_enabled = False  # Flag to control when clicking starts

# Fishing states
class FishingState:
    CASTING = "CASTING"     # Line is cast, waiting for fish to bite
    BITING = "BITING"       # Fish is biting, ready to set the hook
current_state = FishingState.CASTING

tolerance = 3
cast_score = 32
reel_score = 52

cooldown_duration = 3
last_click_time = time.time()

while True:
    # Capture the region of interest from the screen
    with mss() as sct:
        sct_img = sct.grab(roi)
        # Convert to a numpy array and show in a window using cv2
        img = np.array(sct_img)
    
    score = get_img_score(img)
    cv2.putText(img, "Score: {:.2f}".format(score), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if clicking_enabled:
        if time.time() - last_click_time >= cooldown_duration:
            # State machine logic
            if current_state == FishingState.CASTING:
                # Check for casting condition (Step 1)
                if is_activated(score, cast_score, tolerance):
                    pyautogui.click()
                    current_state = FishingState.BITING
                    last_click_time = time.time()
                    print(f"Fish on! Set the hook at {time.strftime('%H:%M:%S')}")

            elif current_state == FishingState.BITING:
                if (is_activated(score, reel_score, tolerance)):
                    pyautogui.click()
                    current_state = FishingState.CASTING
                    last_click_time = time.time()
                    print(f"Fish landed! Recasting at {time.strftime('%H:%M:%S')}")

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

    # Toggle position and clicking on 'p'
    if key == ord('p'):
        x, y = get_mouse_position()
        roi['left'] = x - 70  # Center the capture box on the cursor
        roi['top'] = y - 70   # Center the capture box on the cursor
        clicking_enabled = not clicking_enabled
        print(f"ROI position set to: left={roi['left']}, top={roi['top']}")
        if clicking_enabled:
            current_state = FishingState.CASTING
            pyautogui.click()
            print("Clicking enabled - Press 'p' to pause")
        else:
            print("Clicking paused - Press 'p' to resume")

# Clean up
cv2.destroyAllWindows()