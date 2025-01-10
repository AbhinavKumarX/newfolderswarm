import cv2
import numpy as np

def get_hsv_ranges():
    """Define HSV range for blue color."""
    blue_range = (np.array([100, 100, 100]), np.array([130, 255, 255]))
    return blue_range

def create_mask(img_hsv, color_range):
    """Create a mask for the given color range."""
    return cv2.inRange(img_hsv, *color_range)

def main():
    # Get HSV range for blue color
    blue_range = get_hsv_ranges()
    webcam_video = cv2.VideoCapture(0)

    if not webcam_video.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, video = webcam_video.read()
        if not success:
            print("Error: Could not read frame.")
            break

        # Convert frame to HSV color space
        img_hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
        
        # Create a mask for blue color
        blue_mask = create_mask(img_hsv, blue_range)

        # Highlight blue areas in the original video frame
        blue_highlighted = cv2.bitwise_and(video, video, mask=blue_mask)

        # Display the mask and the video with highlighted blue areas
        cv2.imshow("Blue Mask", blue_mask)
        cv2.imshow("Video Feed with Blue Highlighted", blue_highlighted)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    webcam_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
