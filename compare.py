from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np

# Load the images
img1 = cv2.imread('wait.jpeg')
img2 = cv2.imread('reel.jpeg')

# Convert the images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Calculate the histograms of the two images
hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

# Normalize the histograms
hist1_norm = cv2.normalize(hist1, hist1, alpha=0, beta=1)
hist2_norm = cv2.normalize(hist2, hist2, alpha=0, beta=1)

# Compare the histograms using the correlation method
corr = cv2.compareHist(hist1_norm, hist2_norm, cv2.HISTCMP_CORREL)

# Print the result
print("The correlation between the histograms of the two images is:", corr)

