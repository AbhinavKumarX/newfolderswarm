import cv2
import numpy as np

def get_hsv_ranges():
    """Define HSV range for pink color."""
    pink_range = (np.array([140, 100, 100]), np.array([170, 255, 255]))
    return pink_range

def create_mask(img_hsv, color_range):
    """Create a mask for the given color range."""
    return cv2.inRange(img_hsv, *color_range)

def main():
    # Get HSV range for pink color
    pink_range = get_hsv_ranges()
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
        
        # Create a mask for pink color
        pink_mask = create_mask(img_hsv, pink_range)

        # Highlight pink areas in the original video frame
        pink_highlighted = cv2.bitwise_and(video, video, mask=pink_mask)

        # Display the mask and the video with highlighted pink areas
        cv2.imshow("Pink Mask", pink_mask)
        cv2.imshow("Video Feed with Pink Highlighted", pink_highlighted)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    webcam_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
