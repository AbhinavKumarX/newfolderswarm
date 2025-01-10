import cv2
import numpy as np

# Open the camera feed (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Process the video feed frame by frame
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Resize the frame for consistency
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV range for green color
    lower_green = np.array([35, 40, 40])  # Adjust based on your green color
    upper_green = np.array([85, 255, 255])

    # Create a mask for green
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Invert the green mask to focus on non-green areas (potential white lines)
    non_green_mask = cv2.bitwise_not(green_mask)

    # Use the inverted mask to detect white areas
    white_line = cv2.bitwise_and(frame, frame, mask=non_green_mask)

    # Convert to grayscale for further processing
    gray = cv2.cvtColor(white_line, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to isolate white regions
    _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours of the white regions
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original frame
    for contour in contours:
        if cv2.contourArea(contour) > 50:  # Filter by area to ignore noise
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)  # Red color for lines

    # Display the resulting frames
    cv2.imshow('Camera Feed with White Line Detection', frame)
    cv2.imshow('White Line Mask', threshold)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
