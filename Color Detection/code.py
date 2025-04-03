import cv2
import numpy as np
import time
from picamera2 import Picamera2

# Initialize the Pi Camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

time.sleep(2)  # Allow camera to warm up

while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to OpenCV BGR format
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert frame to HSV

    # Define color ranges
    yellow_lower = np.array([20, 50, 100], dtype=np.uint8)
    yellow_upper = np.array([42, 255, 255], dtype=np.uint8)
    blue_lower = np.array([110, 130, 50], dtype=np.uint8)
    blue_upper = np.array([130, 255, 255], dtype=np.uint8)
    green_lower = np.array([44, 54, 63], dtype=np.uint8)
    green_upper = np.array([90, 255, 255], dtype=np.uint8)
    
    # Create masks for each color
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
    mask_green = cv2.inRange(hsv, green_lower, green_upper)
    
    # Count non-zero pixels in masks
    yellow_pixels = cv2.countNonZero(mask_yellow)
    blue_pixels = cv2.countNonZero(mask_blue)
    green_pixels = cv2.countNonZero(mask_green)
    
    # Determine object placement
    if blue_pixels > 4000:
        print("Detected: BLUE - Place in Position A")
        time.sleep(1)
    elif green_pixels > 4000:
        print("Detected: GREEN - Place in Position B")
        time.sleep(1)
    elif yellow_pixels > 8000:
        print("Detected: YELLOW - Place in Position C")
        time.sleep(1)
    
    # Display masks (for debugging)
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask Yellow', mask_yellow)
    cv2.imshow('Mask Blue', mask_blue)
    cv2.imshow('Mask Green', mask_green)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
