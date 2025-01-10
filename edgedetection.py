import cv2
import numpy as np

# Load the image
image = cv2.imread('path_to_your_image.jpg', cv2.IMREAD_GRAYSCALE)

# Check if image is loaded successfully
if image is None:
    print("Error: Could not open or find the image.")
    exit()

# Apply Canny edge detection
edges = cv2.Canny(image, 100, 200)

# Display the original image and the edge-detected image
cv2.imshow('Original Image', image)
cv2.imshow('Edge Detected Image', edges)

# Wait for a key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()