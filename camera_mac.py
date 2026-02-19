import cv2
import serial
import time
import numpy as np

# --- CONFIGURATION ---
# CHANGE THIS to your Arduino's port! 
# (Check Arduino IDE -> Tools -> Port)
serial_port = '/dev/cu.usbmodem1301' 
baud_rate = 9600

# Connect to Arduino
arduino = None
try:
    arduino = serial.Serial(serial_port, baud_rate)
    time.sleep(2) # Wait for connection
    print(f"Connected to Arduino on {serial_port}")
except Exception as e:
    print(f"WARNING: Arduino not found ({e}). Running camera only.")
    arduino = None

# Start Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Camera not found! Check if it's connected.")
    exit()
print("Camera started successfully")

# Define "Orange" color range for ping pong ball
# Higher saturation to avoid light brown tables
lower_color = np.array([10, 150, 150])   # Lower Orange
upper_color = np.array([25, 255, 255])   # Upper Orange

frame_count = 0

while True:
    try:
        ret, frame = cap.read()
        if not ret: 
            print("End of video or camera disconnected")
            break
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processing frame {frame_count}...")

        # Mirror the frame so "Left" is your Left
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        
        # Color Detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find the ball
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        command = 'N' # Default: Nothing detected

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            
            if radius > 10:
                # Draw circle on screen
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                
                # --- ZONE LOGIC ---
                zone_width = width / 3
                
                if x < zone_width:
                    # ZONE 1: LEFT
                    if arduino:
                        arduino.write(b'L') 
                    cv2.putText(frame, "LEFT (Red)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                elif x < (zone_width * 2):
                    # ZONE 2: CENTER
                    if arduino:
                        arduino.write(b'C')
                    cv2.putText(frame, "CENTER (Both)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    
                else:
                    # ZONE 3: RIGHT
                    if arduino:
                        arduino.write(b'R')
                    cv2.putText(frame, "RIGHT (Green)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show video feed
        try:
            cv2.imshow("Goalie Vision", frame)
            cv2.imshow("Color Isolation (Mask)", mask)  # Shows what the camera detects
        except Exception as e:
            print(f"Error displaying windows: {e}")

        # Press 'q' to quit
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
            
    except Exception as e:
        print(f"Error in main loop: {e}")
        import traceback
        traceback.print_exc()
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()