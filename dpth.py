import numpy as np
import cv2

# Define object-specific variables
focal = 1080  # Focal length (arbitrary, needs calibration)
real_diameter = 4  # Real-world diameter of the ball in cm

# Calculate distance from the camera
def get_dist(radius, image):
    if radius > 0:
        pixel_diameter = radius * 2  # Convert radius to diameter
        dist = (real_diameter * focal) / pixel_diameter  # Distance formula
    else:
        dist = 0

    # Display distance on the image
    image = cv2.putText(image, 'Distance from Camera in CM:', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,  
                        0.6, (0, 0, 255), 2, cv2.LINE_AA)
    image = cv2.putText(image, f'{dist:.2f} cm', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 0, 255), 2, cv2.LINE_AA)
    return image

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access the camera")
    exit()

cv2.namedWindow('Object Distance Measure', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Distance Measure', 700, 600)

# Loop to capture video frames
while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define red color range in HSV
    lower1 = np.array([0, 170, 100])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 170, 100])
    upper2 = np.array([180, 255, 255])
    
    # Create mask for red color
    mask1 = cv2.inRange(hsv_img, lower1, upper1)
    mask2 = cv2.inRange(hsv_img, lower2, upper2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Apply Gaussian blur to smooth edges
    blurred = cv2.GaussianBlur(mask, (9, 9), 2)

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.2, 50, param1=50, param2=30, minRadius=10, maxRadius=100)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])  # Circle center
            radius = i[2]  # Circle radius
            
            # Draw the detected circle
            cv2.circle(img, center, radius, (0, 255, 0), 3)
            cv2.circle(img, center, 2, (255, 0, 0), 3)  # Center point
            
            # Calculate and display the distance
            img = get_dist(radius, img)
            break  # Only process the first detected circle
    
    cv2.imshow('Object Distance Measure', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()