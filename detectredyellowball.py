import cv2
import numpy as np

def get_hsv_ranges():
    """Define HSV ranges for red and yellow colors."""
    red_ranges = [
        (np.array([0, 170, 100]), np.array([10, 255, 255])),
        (np.array([170, 170, 100]), np.array([180, 255, 255]))
    ]
    yellow_range = (np.array([20, 170, 100]), np.array([30, 255, 255]))
    return red_ranges, yellow_range

def create_combined_mask(img_hsv, red_ranges, yellow_range):
    """Create a combined mask for red and yellow colors."""
    red_mask = sum(cv2.inRange(img_hsv, lower, upper) for lower, upper in red_ranges)
    yellow_mask = cv2.inRange(img_hsv, *yellow_range)
    return red_mask | yellow_mask

def detect_and_draw_circles(video, mask):
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

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, radius = circle
            cv2.circle(video, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(video, (x, y), 3, (0, 0, 255), -1)
            cv2.putText(video, f"({x}, {y})", (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def main():
    red_ranges, yellow_range = get_hsv_ranges()
    webcam_video = cv2.VideoCapture(0)

    if not webcam_video.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, video = webcam_video.read()
        if not success:
            print("Error: Could not read frame.")
            break

        img_hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
        combined_mask = create_combined_mask(img_hsv, red_ranges, yellow_range)
        detect_and_draw_circles(video, combined_mask)

        cv2.imshow("Mask Image", combined_mask)
        cv2.imshow("Video Feed", video)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
