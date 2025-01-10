import cv2
import numpy as np

# Read the image
image = cv2.imread('your_image.jpg')
output = image.copy()

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define lower and upper range for red in HSV
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

# Threshold the image to get only red colors
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)

# Reduce noise
red_mask = cv2.GaussianBlur(red_mask, (9, 9), 2)

# Detect circles using HoughCircles
circles = cv2.HoughCircles(
    red_mask, 
    cv2.HOUGH_GRADIENT, 
    dp=1, 
    minDist=20,
    param1=50, 
    param2=30, 
    minRadius=0, 
    maxRadius=0
)

# Draw the circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Circle outline
        cv2.circle(output, (i[0], i[1]), 2, (255, 0, 0), 3)  # Circle center

# Show the result
cv2.imshow("Detected Red Circles", output)
cv2.waitKey(0)
cv2.destroyAllWindows()