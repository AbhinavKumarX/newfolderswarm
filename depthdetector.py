import cv2
import torch
import numpy as np
from PIL import Image
from torchvision.transforms import transforms

# Load the MiDaS model
model_type = "DPT_Large"  # Options: DPT_Large, DPT_Hybrid, MiDaS_small
model = torch.hub.load("intel-isl/MiDaS", model_type)
model.eval()

# Load transforms for MiDaS
transform = (
    torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform
    if model_type.startswith("DPT")
    else torch.hub.load("intel-isl/MiDaS", "transforms").small_transform
)

# Function to detect the red ball
def detect_red_ball(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the red color range in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Mask for red color
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    red_mask = mask1 + mask2

    # Find contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 500:  # Minimum size filter
            x, y, w, h = cv2.boundingRect(largest_contour)
            return (x, y, w, h)
    return None

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Get the bounding box of the red ball
    ball_region = detect_red_ball(frame)
    if ball_region:
        x, y, w, h = ball_region

        # Crop the ball region and preprocess for MiDaS
        ball_frame = frame[y : y + h, x : x + w]
        input_image = cv2.cvtColor(ball_frame, cv2.COLOR_BGR2RGB)
        input_image_pil = Image.fromarray(input_image)  # Convert to PIL image

        # Apply transform
        input_image_tensor = transform(input_image_pil).unsqueeze(0)  # Add batch dimension

        # Predict depth using MiDaS
        with torch.no_grad():
            prediction = model(input_image_tensor)
            depth_map = prediction.squeeze().cpu().numpy()

        # Get the average depth in the region
        avg_depth = np.mean(depth_map)

        # Display the depth and draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Depth: {avg_depth:.2f}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    # Show the frame
    cv2.imshow("Depth Estimation", frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
