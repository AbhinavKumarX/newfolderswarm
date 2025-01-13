import cv2
import numpy as np

def get_hsv_ranges():
    """Define HSV ranges for red and pink colors."""
    # Define red HSV ranges
    red_ranges = [
        (np.array([0, 170, 100]), np.array([10, 255, 255])),
        (np.array([170, 170, 100]), np.array([180, 255, 255]))
    ]
    # Define pink HSV range
    pink_range = (np.array([140, 100, 100]), np.array([170, 255, 255]))

    return red_ranges, pink_range

def create_combined_mask(img_hsv, red_ranges, pink_range):
    """Create a combined mask for red and pink colors."""
    # Combine red masks
    red_mask = sum(cv2.inRange(img_hsv, lower, upper) for lower, upper in red_ranges)
    # Create pink mask
    pink_mask = cv2.inRange(img_hsv, *pink_range)

    return red_mask, pink_mask

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
        minRadius=40,
        maxRadius=200
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

def detect_pink_center(video, mask):
    """Detect the center of the pink-colored object using moments."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate moments
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
            # Draw center point and contour
            cv2.drawContours(video, [largest_contour], -1, (0, 255, 255), 2)
            cv2.circle(video, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.putText(video, f"Pink ({center_x}, {center_y})", (center_x - 50, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            return center_x, center_y
    return -1, -1

def process_center_position(center_x, center_y, frame_width, frame_height, color_name):
    """Process the position of the detected center and print coordinates relative to screen center."""
    if center_x == -1 or center_y == -1:
        print(f"{color_name} center not detected: Object not in frame.")
        return

    # Calculate relative coordinates
    screen_center_x = frame_width // 2
    screen_center_y = frame_height // 2

    relative_x = center_x - screen_center_x
    relative_y = screen_center_y - center_y  # Invert Y-axis to match standard cartesian coordinates

    print(f"{color_name} object detected at relative coordinates: ({relative_x}, {relative_y})")

def main():
    red_ranges, pink_range = get_hsv_ranges()
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

        # Create masks for red and pink
        red_mask, pink_mask = create_combined_mask(img_hsv, red_ranges, pink_range)

        # Detect and draw circles for red
        red_center_x, red_center_y = detect_and_draw_circles(video, red_mask, "Red")

        # Detect center for pink objects
        pink_center_x, pink_center_y = detect_pink_center(video, pink_mask)

        # Process center positions for red and pink
        process_center_position(red_center_x, red_center_y, frame_width, frame_height, "Red")
        process_center_position(pink_center_x, pink_center_y, frame_width, frame_height, "Pink")

        # Display the video feed and masks
        combined_mask = red_mask | pink_mask
        cv2.imshow("Mask Image", combined_mask)
        cv2.imshow("Video Feed", video)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
