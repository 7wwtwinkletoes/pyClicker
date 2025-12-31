import cv2
import numpy as np
import pyautogui

# Create a blank image with white background
width, height = 200, 100
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Define the font properties
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.5
font_thickness = 2

# Get the size of the text
text = "running"
(text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

# Calculate the position to center the text on the image
text_x = int((width - text_width) / 2)
text_y = int((height + text_height) / 2)

# Draw the text on the image
cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

# Display the image in a window
cv2.imshow("Window", image)

# Wait for key press and check if 'q' is pressed
while True:
    pyautogui.click()


    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Close the window
cv2.destroyAllWindows()
