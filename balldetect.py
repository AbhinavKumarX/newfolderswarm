import cv2
import numpy as np

def get_hsv_ranges():
    """Define HSV ranges for red, yellow, and pink colors."""
    red_ranges = [
        (np.array([0, 170, 100]), np.array([10, 255, 255])),
        (np.array([170, 170, 100]), np.array([180, 255, 255]))
    ]
    yellow_range = (np.array([20, 170, 100]), np.array([30, 255, 255]))
    pink_range = (np.array([140, 100, 100]), np.array([170, 255, 255]))
    return red_ranges, yellow_range, pink_range

def create_combined_mask(img_hsv, red_ranges, yellow_range, pink_range):
    """Create a combined mask for red, yellow, and pink colors."""
    red_mask = sum(cv2.inRange(img_hsv, lower, upper) for lower, upper in red_ranges)
    yellow_mask = cv2.inRange(img_hsv, *yellow_range)
    pink_mask = cv2.inRange(img_hsv, *pink_range)
    return red_mask, yellow_mask, pink_mask

def detect_and_draw_circles(video, mask, color_name):
    """Detect circles in the mask and draw them on the video frame."""
    blurred_mask = cv2.GaussianBlur(mask, (9, 9), 2)
    circles = cv2.HoughCircles(
        blurred_mask,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=20,
        maxRadius=100
    )

    center_x, center_y = -1, -1  # Default values if no circle is detected

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, radius = circle
            cv2.circle(video, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(video, (x, y), 3, (0, 0, 255), -1)
            cv2.putText(video, f"{color_name} ({x}, {y})", (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            center_x, center_y = x, y

    return center_x, center_y

def process_center_position(center_x, center_y, frame_width, color_name):
    """Process the position of the detected circle's center."""
    if center_x == -1:
        print(f"{color_name} center not detected: Object not in frame. Turn right.")
        return

    # Define left, center, and right zones
    left_zone = frame_width // 3
    right_zone = 2 * frame_width // 3

    if center_x < left_zone:
        print(f"{color_name} object in the left zone. Consider turning left.")
    elif center_x > right_zone:
        print(f"{color_name} object in the right zone. Consider turning right.")
    else:
        print(f"{color_name} object in the center zone. Stay on course.")

def main():
    red_ranges, yellow_range, pink_range = get_hsv_ranges()
    webcam_video = cv2.VideoCapture(0)

    if not webcam_video.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, video = webcam_video.read()
        if not success:
            print("Error: Could not read frame.")
            break

        # Get frame dimensions
        frame_height, frame_width, _ = video.shape

        # Convert frame to HSV color space
        img_hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)

        # Create masks for red, yellow, and pink
        red_mask, yellow_mask, pink_mask = create_combined_mask(img_hsv, red_ranges, yellow_range, pink_range)

        # Detect and draw circles for each color
        red_center_x, red_center_y = detect_and_draw_circles(video, red_mask, "Red")
        yellow_center_x, yellow_center_y = detect_and_draw_circles(video, yellow_mask, "Yellow")
        pink_center_x, pink_center_y = detect_and_draw_circles(video, pink_mask, "Pink")

        # Process center positions for red, yellow, and pink
        process_center_position(red_center_x, red_center_y, frame_width, "Red")
        process_center_position(yellow_center_x, yellow_center_y, frame_width, "Yellow")
        process_center_position(pink_center_x, pink_center_y, frame_width, "Pink")

        # Display the video feed and masks
        combined_mask = red_mask | yellow_mask | pink_mask
        cv2.imshow("Mask Image", combined_mask)
        cv2.imshow("Video Feed", video)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
