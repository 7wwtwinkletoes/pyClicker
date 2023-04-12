from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from PIL import Image

def get_score(image_path):
    ref_img = cv2.imread(image_path)
    hsv_ref_img = cv2.cvtColor(ref_img, cv2.COLOR_BGR2HSV)
    ref_green = hsv_ref_img[:,:,1]
    mean_green_ref = cv2.mean(ref_green)[0]

    return mean_green_ref



for i in range(1,5):
    print(get_score(f'step_{i}.jpg'))





