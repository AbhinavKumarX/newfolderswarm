import cv2
import numpy as np

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper range for red color
    lower_red1 = np.array([0, 120, 70])    # Lower range of red
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])  # Upper range of red
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color (accounting for wrap-around in hue values)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2

    # Bitwise-AND mask with the original frame
    red_only = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Convert the isolated red regions to grayscale
    gray = cv2.cvtColor(red_only, cv2.COLOR_BGR2GRAY)

    # Blur the grayscale image to reduce noise
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Apply Hough Circle Transform to detect circles
    detected_circles = cv2.HoughCircles(
        gray_blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=20, 
        param1=50, 
        param2=30, 
        minRadius=1, 
        maxRadius=40
    )

    # Draw the detected circles on the red-only image
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle
            cv2.circle(red_only, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center
            cv2.circle(red_only, (a, b), 1, (0, 0, 255), 3)

    # Display the red-isolated image instead of the original frame
    cv2.imshow("Detected Red Circles", red_only)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()