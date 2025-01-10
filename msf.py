import cv2
import numpy as np

# Specifying upper and lower ranges of color to detect in HSV format
lower_red1 = np.array([0, 170, 100])    # Lower range of red
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 170, 100])  # Upper range of red
upper_red2 = np.array([180, 255, 255])

# Capturing webcam footage
webcam_video = cv2.VideoCapture(0)

if not webcam_video.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    success, video = webcam_video.read()  # Reading webcam footage
    if not success:
        print("Error: Could not read frame.")
        break

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)  # Converting BGR image to HSV format

    mask1 = cv2.inRange(img, lower_red1, upper_red1)  # Masking the image to find our color
    mask2 = cv2.inRange(img, lower_red2, upper_red2)
    red_mask = mask1 | mask2

    mask_contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Finding contours

    # Drawing bounding boxes for large contours
    for mask_contour in mask_contours:
        if cv2.contourArea(mask_contour) > 500:
            x, y, w, h = cv2.boundingRect(mask_contour)
            cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cv2.imshow("Mask Image", red_mask)  # Displaying mask image
    cv2.imshow("Video Feed", video)    # Displaying webcam image

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
webcam_video.release()
cv2.destroyAllWindows()
