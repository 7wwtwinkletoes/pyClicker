import cv2
import numpy as np
import sys
import os

def get_img_score(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_green = hsv_img[:,:,1]
    return cv2.mean(img_green)[0]

def analyze_image(image_path):
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image: {image_path}")
        return
    
    # Get HSV channels for detailed analysis
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Get mean values for each channel
    h_mean = cv2.mean(h)[0]
    s_mean = cv2.mean(s)[0]
    v_mean = cv2.mean(v)[0]
    
    # Calculate percentage of pixels with high value (brightness)
    high_value_pixels = np.sum(v > 160)  # Count pixels brighter than 160
    high_value_ratio = high_value_pixels / (v.shape[0] * v.shape[1])
    
    # Calculate percentage of pixels in green-yellow hue range
    green_yellow_pixels = np.sum((h >= 60) & (h <= 80))
    green_yellow_ratio = green_yellow_pixels / (h.shape[0] * h.shape[1])
    
    # Display results
    print(f"\nAnalysis for {os.path.basename(image_path)}:")
    print(f"HSV Means: H={h_mean:.2f}, S={s_mean:.2f}, V={v_mean:.2f}")
    print(f"High Value Ratio: {high_value_ratio:.3f}")
    print(f"Green-Yellow Ratio: {green_yellow_ratio:.3f}")
    
    # Display the image with analysis
    info_text = f"H={h_mean:.1f} S={s_mean:.1f} V={v_mean:.1f}"
    ratio_text = f"HV={high_value_ratio:.3f} GY={green_yellow_ratio:.3f}"
    cv2.putText(img, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, ratio_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow(os.path.basename(image_path), img)
    
    return {
        'hsv': (h_mean, s_mean, v_mean),
        'ratios': (high_value_ratio, green_yellow_ratio)
    }

def main():
    assets_dir = "assets"
    image_files = ["step_1.jpg", "step_2.jpg", "step_3.jpg", "step_4.jpg"]
    results = {}
    
    print("Analyzing fishing step images...")
    
    for image_file in image_files:
        image_path = os.path.join(assets_dir, image_file)
        results[image_file] = analyze_image(image_path)
    
    print("\nSummary:")
    print("-" * 70)
    for image_file, data in results.items():
        h, s, v = data['hsv']
        hv_ratio, gy_ratio = data['ratios']
        print(f"{image_file:10}: HSV=({h:.1f}, {s:.1f}, {v:.1f}), ", end="")
        print(f"HighValue={hv_ratio:.3f}, GreenYellow={gy_ratio:.3f}")
    
    print("\nClick vs No-Click Analysis:")
    print("-" * 70)
    click_states = ["step_1.jpg", "step_3.jpg"]
    no_click_states = ["step_2.jpg", "step_4.jpg"]
    
    click_hv = [results[f]['ratios'][0] for f in click_states]
    click_gy = [results[f]['ratios'][1] for f in click_states]
    no_click_hv = [results[f]['ratios'][0] for f in no_click_states]
    no_click_gy = [results[f]['ratios'][1] for f in no_click_states]
    
    print("\nClicking States (1 & 3):")
    print(f"High Value Ratio Range: {min(click_hv):.3f} - {max(click_hv):.3f}")
    print(f"Green-Yellow Ratio Range: {min(click_gy):.3f} - {max(click_gy):.3f}")
    
    print("\nNon-Clicking States (2 & 4):")
    print(f"High Value Ratio Range: {min(no_click_hv):.3f} - {max(no_click_hv):.3f}")
    print(f"Green-Yellow Ratio Range: {min(no_click_gy):.3f} - {max(no_click_gy):.3f}")
    
    print("\nPress any key to close windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()