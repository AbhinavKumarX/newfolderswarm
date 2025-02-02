import cv2
import numpy as np
import cv2.aruco as aruco

def detect_aruco_from_cam():
    """
    Detects ArUco markers in real-time using a webcam and marks them with their IDs.
    Press 'q' to exit the webcam feed.
    """
    # Open the webcam (0 for default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Load the predefined ArUco dictionary
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect markers
        corners, ids, _ = detector.detectMarkers(gray)

        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            
            for i, marker_id in enumerate(ids):
                x, y = int(corners[i][0][0][0]), int(corners[i][0][0][1])
                cv2.putText(frame, f"ID: {marker_id[0]}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Show the output
        cv2.imshow("ArUco Marker Detection", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_aruco_from_cam()
