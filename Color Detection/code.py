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

    # Define HSV color ranges
    yellow_lower = np.array([20, 50, 100], dtype=np.uint8)
    yellow_upper = np.array([42, 255, 255], dtype=np.uint8)

    blue_lower = np.array([100, 130, 50], dtype=np.uint8)
    blue_upper = np.array([130, 255, 255], dtype=np.uint8)

    green_lower = np.array([44, 54, 63], dtype=np.uint8)
    green_upper = np.array([90, 255, 255], dtype=np.uint8)

    # Red has two ranges in HSV (wraps around 180)
    red_lower1 = np.array([0, 100, 100], dtype=np.uint8)
    red_upper1 = np.array([10, 255, 255], dtype=np.uint8)
    red_lower2 = np.array([160, 100, 100], dtype=np.uint8)
    red_upper2 = np.array([180, 255, 255], dtype=np.uint8)

    white_lower = np.array([0, 0, 200], dtype=np.uint8)
    white_upper = np.array([180, 55, 255], dtype=np.uint8)

    black_lower = np.array([0, 0, 0], dtype=np.uint8)
    black_upper = np.array([180, 255, 50], dtype=np.uint8)

    # Create masks
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
    mask_green = cv2.inRange(hsv, green_lower, green_upper)
    mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_white = cv2.inRange(hsv, white_lower, white_upper)
    mask_black = cv2.inRange(hsv, black_lower, black_upper)

    # Count non-zero pixels
    yellow_pixels = cv2.countNonZero(mask_yellow)
    blue_pixels = cv2.countNonZero(mask_blue)
    green_pixels = cv2.countNonZero(mask_green)
    red_pixels = cv2.countNonZero(mask_red)
    white_pixels = cv2.countNonZero(mask_white)
    black_pixels = cv2.countNonZero(mask_black)

    
    # Determine detected color
    if blue_pixels > 4000:
        print("Detected: BLUE - Place in Position A")
        time.sleep(1)
    elif green_pixels > 4000:
        print("Detected: GREEN - Place in Position B")
        time.sleep(1)
    elif yellow_pixels > 8000:
        print("Detected: YELLOW - Place in Position C")
        time.sleep(1)
    elif red_pixels > 4000:
        print("Detected: RED - Place in Position D")
        time.sleep(1)
    elif white_pixels > 4000:
        print("Detected: WHITE - Place in Position E")
        time.sleep(1)
    elif black_pixels > 4000:
        print("Detected: BLACK - Place in Position F")
        time.sleep(1)
    
    # Display masks (for debugging)
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
