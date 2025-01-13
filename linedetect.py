import cv2
import apriltag
import numpy as np

# Define the real-world size of the AprilTag marker (in meters)
MARKER_SIZE = 0.05  # Example: 5 cm

# Camera intrinsic parameters (replace with your calibration values)
CAMERA_MATRIX = np.array([[1000, 0, 640],
                          [0, 1000, 360],
                          [0, 0, 1]], dtype=np.float32)
DIST_COEFFS = np.zeros((4, 1))  # Assume no distortion for simplicity

def calculate_distance(tag_size, corners):
    """
    Calculate the distance from the camera to the AprilTag.
    """
    # Get top-left, top-right, bottom-right, and bottom-left corners
    top_left, top_right, bottom_right, bottom_left = corners

    # Calculate marker width and height in pixels
    marker_width_px = np.linalg.norm(top_right - top_left)
    marker_height_px = np.linalg.norm(bottom_right - top_right)

    # Average size for stability
    marker_size_px = (marker_width_px + marker_height_px) / 2

    # Distance calculation using the pinhole camera model
    focal_length = CAMERA_MATRIX[0, 0]  # Focal length (fx)
    distance = (tag_size * focal_length) / marker_size_px

    return distance

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize AprilTag detector
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the image
    tags = detector.detect(gray)

    for tag in tags:
        # Extract the corners of the detected tag
        corners = tag.corners
        top_left, top_right, bottom_right, bottom_left = corners

        # Draw the detected tag
        corners = np.int32(corners)
        cv2.polylines(frame, [corners], isClosed=True, color=(0, 255, 0), thickness=2)

        # Calculate the distance
        distance = calculate_distance(MARKER_SIZE, corners)
        center_x, center_y = int(tag.center[0]), int(tag.center[1])
        cv2.putText(frame, f"Distance: {distance:.2f}m", (center_x, center_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the result
    cv2.imshow("AprilTag Distance", frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
