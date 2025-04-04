**Color Detection Algorithm Using Raspberry Pi and Pi Camera Module** 

**1. Introduction**  
This report details the implementation and workflow of a real-time color detection algorithm using a Raspberry Pi and a Pi Camera module. The algorithm captures live video frames, processes them to detect specific colors (yellow, blue, and green), and provides instructions based on the detected colors.

---

**2. System Overview**  
The system consists of the following components:
- **Hardware:** Raspberry Pi, Pi Camera Module
- **Software:** OpenCV for image processing, NumPy for numerical operations, and Picamera2 for camera interfacing

---

**3. Algorithm Flow Description**  
The following steps explain the algorithm's execution flow:

### **Step 1: Initialize the Pi Camera**  
- The `Picamera2` module is used to interface with the Raspberry Pi camera.
- The camera is configured with a preview resolution of 640x480 pixels and RGB888 format.
- The camera starts, and a **2-second delay** is added to allow it to warm up.

```python
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)
```

### **Step 2: Capture and Process Frames**  
- The camera continuously captures frames and converts them to OpenCV’s BGR format for processing.
- The BGR frame is converted to **HSV (Hue, Saturation, Value)** format since HSV is more effective for color-based segmentation.

```python
frame = picam2.capture_array()
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

### **Step 3: Define Color Ranges**  
- HSV ranges are defined for **yellow, blue, and green** colors.
- These ranges allow the algorithm to create color masks and filter specific colors.

```python
yellow_lower = np.array([20, 50, 100], dtype=np.uint8)
yellow_upper = np.array([42, 255, 255], dtype=np.uint8)
blue_lower = np.array([110, 130, 50], dtype=np.uint8)
blue_upper = np.array([130, 255, 255], dtype=np.uint8)
green_lower = np.array([44, 54, 63], dtype=np.uint8)
green_upper = np.array([90, 255, 255], dtype=np.uint8)
```

### **Step 4: Create Masks and Count Pixels**  
- The algorithm applies **cv2.inRange()** to filter the specified colors and create binary masks.

```python
mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
mask_green = cv2.inRange(hsv, green_lower, green_upper)
```

- The algorithm then counts the number of nonzero pixels for each color mask.

```python
yellow_pixels = cv2.countNonZero(mask_yellow)
blue_pixels = cv2.countNonZero(mask_blue)
green_pixels = cv2.countNonZero(mask_green)
```

### **Step 5: Object Placement Decision**  
- The algorithm determines where to place the object based on the detected color.
- If **blue pixels > 4000**, the object is placed in Position A.
- If **green pixels > 4000**, the object is placed in Position B.
- If **yellow pixels > 8000**, the object is placed in Position C.
- A **5-second delay** prevents rapid printing of messages.

```python
if blue_pixels > 4000:
    print("Detected: BLUE - Place in Position A")
    time.sleep(5)
elif green_pixels > 4000:
    print("Detected: GREEN - Place in Position B")
    time.sleep(5)
elif yellow_pixels > 8000:
    print("Detected: YELLOW - Place in Position C")
    time.sleep(5)
```

### **Step 6: Display the Frame and Masks**  
- The frame is displayed in a window to debug the algorithm.
- The individual color masks are also displayed for better visualization.
- The loop continues capturing frames until the user presses the ‘q’ key.

```python
cv2.imshow('Frame', frame)
cv2.imshow('Mask Yellow', mask_yellow)
cv2.imshow('Mask Blue', mask_blue)
cv2.imshow('Mask Green', mask_green)
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

### **Step 7: Cleanup and Exit**  
- When the loop exits, all OpenCV windows are closed, and the camera is stopped.

```python
cv2.destroyAllWindows()
picam2.stop()
```
### Testing 
![Screenshot 2025-04-03 172432](https://github.com/user-attachments/assets/074fe6ed-a5f1-4878-9bfb-c98812c14845)

![green](https://github.com/user-attachments/assets/fa4804e2-3bf1-4952-a753-b346c0fd4633)



---


**5. Conclusion**  
This color detection algorithm effectively identifies objects of specific colors using a Raspberry Pi and Pi Camera module. The flow of execution includes camera initialization, frame capturing, color filtering, pixel counting, and decision-making. Minor issues were identified and corrected to ensure smooth operation. Future improvements could include adaptive color thresholding and enhanced noise reduction techniques.

---

