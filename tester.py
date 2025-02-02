import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep

# GPIO setup for motor control
in1 = 24
in2 = 23
in3 = 21
in4 = 22
en = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
p = GPIO.PWM(en, 1000)
p.start(50)

# HSV ranges for colors
def get_hsv_ranges():
    red_ranges = [
        (np.array([0, 170, 100]), np.array([10, 255, 255])),
        (np.array([170, 170, 100]), np.array([180, 255, 255]))
    ]
    pink_range = (np.array([140, 100, 100]), np.array([170, 255, 255]))
    white_range = (np.array([0, 0, 200]), np.array([180, 50, 255]))
    return red_ranges, pink_range, white_range

# Create combined mask for the colors
def create_combined_mask(img_hsv, red_ranges, pink_range, white_range):
    red_mask = sum(cv2.inRange(img_hsv, lower, upper) for lower, upper in red_ranges)
    pink_mask = cv2.inRange(img_hsv, *pink_range)
    white_mask = cv2.inRange(img_hsv, *white_range)
    return red_mask, pink_mask, white_mask

# Process detected positions
def process_center_position(center_x, center_y, frame_width, color_name):
    screen_center_x = frame_width // 2
    tolerance = 15

    if center_x == -1:
        print(f"{color_name} not detected. Turning left.")
        move_motor("fl")
    elif center_x < screen_center_x - tolerance:
        print(f"{color_name} to the left. Turning left.")
        move_motor("fl")
    elif center_x > screen_center_x + tolerance:
        print(f"{color_name} to the right. Turning right.")
        move_motor("fr")
    else:
        print(f"{color_name} centered. Moving forward.")
        move_motor("f")

# Motor movement commands
def move_motor(command):
    if command == "f":
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
    elif command == "fl":
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
    elif command == "fr":
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
    elif command == "stop":
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

# Main function
def main():
    red_ranges, pink_range, white_range = get_hsv_ranges()
    webcam_video = cv2.VideoCapture(0)

    if not webcam_video.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while True:
            success, video = webcam_video.read()
            if not success:
                print("Error: Could not read frame.")
                break

            frame_height, frame_width, _ = video.shape
            img_hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)
            red_mask, pink_mask, white_mask = create_combined_mask(img_hsv, red_ranges, pink_range, white_range)

            # Detect red
            red_center_x, red_center_y = detect_center(red_mask)
            process_center_position(red_center_x, red_center_y, frame_width, "Red")

            # Detect pink
            pink_center_x, pink_center_y = detect_center(pink_mask)
            process_center_position(pink_center_x, pink_center_y, frame_width, "Pink")

            # Display frames
            combined_mask = red_mask | pink_mask | white_mask
            cv2.imshow("Mask Image", combined_mask)
            cv2.imshow("Video Feed", video)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        webcam_video.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()

# Detect center using contours
def detect_center(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
            return center_x, center_y
    return -1, -1

if __name__ == "__main__":
    main()