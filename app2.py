import cv2
from mss import mss
import numpy as np
import pyautogui
import time
import datetime


def get_image_features(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Calculate ratios
    high_value_pixels = np.sum(v > 160)
    high_value_ratio = high_value_pixels / (v.shape[0] * v.shape[1])
    
    green_yellow_pixels = np.sum((h >= 60) & (h <= 80))
    green_yellow_ratio = green_yellow_pixels / (h.shape[0] * h.shape[1])
    
    # Get mean values
    h_mean = cv2.mean(h)[0]
    s_mean = cv2.mean(s)[0]
    v_mean = cv2.mean(v)[0]
    
    return {
        'high_value_ratio': high_value_ratio,
        'green_yellow_ratio': green_yellow_ratio,
        'hsv_means': (h_mean, s_mean, v_mean)
    }

# Function to get current mouse position
def get_mouse_position():
    x, y = pyautogui.position()
    return x, y

# Define the coordinates and size of the region of interest (ROI)
print("\nMove your mouse to where you want to capture and press 'p' to set position and start clicking")
roi = {'left': 843, 'top': 634, 'width': 100, 'height': 100}  # default values
clicking_enabled = False  # Flag to control when clicking starts

# Fishing states
class FishingState:
    CASTING = "CASTING"     # Line is cast, waiting for fish to bite
    BITING = "BITING"       # Fish is biting, ready to set the hook

# Set the cooldown duration (in seconds)
cooldown_duration = 2

# Feature thresholds based on image analysis
REEL_HIGH_VALUE_MIN = 0.85    # Step 3 high value ratio minimum
REEL_GREEN_YELLOW_MIN = 0.08  # Step 3 green-yellow ratio minimum
REEL_SAT_MIN = 45            # Step 3 saturation minimum

CAST_HIGH_VALUE_MIN = 0.5    # Step 1 high value ratio minimum
CAST_SAT_MAX = 15           # Step 1 low saturation maximum

# Set the time of the last click
last_click_time = time.time()
current_state = FishingState.CASTING

score_display_position = (0, 25)
score_display_font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    # Capture the region of interest from the screen
    with mss() as sct:
        sct_img = sct.grab(roi)
        # Convert to a numpy array and show in a window using cv2
        img = np.array(sct_img)
    
    features = get_image_features(img)
    high_value_ratio = features['high_value_ratio']
    green_yellow_ratio = features['green_yellow_ratio']
    h_mean, s_mean, v_mean = features['hsv_means']
    
    # Display the image features for debugging
    if img is not None:
        print(f"HV: {high_value_ratio:.3f}, GY: {green_yellow_ratio:.3f}, S: {s_mean:.1f}", end='\r')

    # Check if clicking is enabled and cooldown has passed
    if clicking_enabled:
        if time.time() - last_click_time >= cooldown_duration:
            # State machine logic
            if current_state == FishingState.CASTING:
                cv2.putText(img, f"HV: {high_value_ratio:.3f} (CASTING...)", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # Check for casting condition (Step 1)
                if high_value_ratio >= CAST_HIGH_VALUE_MIN and s_mean <= CAST_SAT_MAX:
                    pyautogui.click()
                    current_state = FishingState.BITING
                    last_click_time = time.time()
                    print(f"Fish on! Set the hook at {time.strftime('%H:%M:%S')}")

            elif current_state == FishingState.BITING:
                cv2.putText(img, f"HV: {high_value_ratio:.3f} GY: {green_yellow_ratio:.3f} (FISH ON!)", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)
                # Check for reeling condition (Step 3)
                if (high_value_ratio >= REEL_HIGH_VALUE_MIN and 
                    green_yellow_ratio >= REEL_GREEN_YELLOW_MIN and 
                    s_mean >= REEL_SAT_MIN):
                    pyautogui.click()
                    last_click_time = time.time()
                    current_state = FishingState.CASTING
                    print(f"Fish landed! Recasting at {time.strftime('%H:%M:%S')}")

        else:
            cv2.putText(img, f"COOLDOWN - {current_state}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    else:
        cv2.putText(img, f"PAUSED", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)



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
        roi['left'] = x - 50  # Center the capture box on the cursor
        roi['top'] = y - 50   # Center the capture box on the cursor
        clicking_enabled = not clicking_enabled
        print(f"ROI position set to: left={roi['left']}, top={roi['top']}")
        if clicking_enabled:
            current_state = FishingState.CASTING
            pyautogui.click()
            print("Clicking enabled - Press 'p' to pause")
        else:
            print("Clicking paused - Press 'p' to resume")
        
    # Display current mouse position and status
    x, y = get_mouse_position()
    status = "ACTIVE" if clicking_enabled else "PAUSED"
    cv2.putText(img, f"Mouse: ({x}, {y}) - {status}", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Clean up
cv2.destroyAllWindows()
