import cv2
import numpy as np

def get_hsv_ranges():
    """Define HSV ranges for red, pink, and white colors."""
 
    # Define red HSV ranges
    red_ranges = [
        (np.array([0, 170, 100]), np.array([10, 255, 255])),
        (np.array([170, 170, 100]), np.array([180, 255, 255]))
    ]

    # Define pink HSV range
    pink_range = (np.array([140, 100, 100]), np.array([170, 255, 255]))

    # Define white HSV range
    white_range = (np.array([0, 0, 200]), np.array([180, 50, 255]))

    return red_ranges, pink_range, white_range

def create_combined_mask(img_hsv, red_ranges, pink_range, white_range):
    """Create a combined mask for red, pink, and white colors."""
    # Combine red masks
    red_mask = sum(cv2.inRange(img_hsv, lower, upper) for lower, upper in red_ranges)
    # Create pink mask
    pink_mask = cv2.inRange(img_hsv, *pink_range)
    white_mask = cv2.inRange(img_hsv, *white_range)

    return red_mask, pink_mask, white_mask

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
        maxRadius=150
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

def detect_white_dots(video, mask, frame_center_x, frame_width_tolerance):
    """Detect white dots in the specified range around the screen center and count them."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dot_count = 0

    for contour in contours:
        if cv2.contourArea(contour) < 10:  # Ignore very small areas
            continue

        x, y, w, h = cv2.boundingRect(contour)
        dot_center_x = x + w // 2

        if abs(dot_center_x - frame_center_x) <= frame_width_tolerance:
            dot_count += 1
            cv2.circle(video, (dot_center_x, y + h // 2), 2, (0, 255, 0), -1)  # Point-sized dot

    if dot_count > 0:
        cv2.putText(video, f"White Dots: {dot_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return dot_count

def detect_pink_center(video, mask, min_area=500):
    """Detect the center of a sufficiently large pink-colored object using moments."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        # Check if the area of the largest contour meets the minimum area requirement
        if cv2.contourArea(largest_contour) >= min_area:
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
    """Process the position of the detected center and provide movement commands."""
    screen_center_x = frame_width // 2
    screen_center_y = frame_height // 2

    if center_x == -1 or center_y == -1:
        # Object not in frame
        print(f"{color_name} center not detected: Object not in frame. Turning left.")
        return "fl"

    # Calculate relative coordinates
    relative_x = center_x - screen_center_x
    relative_y = screen_center_y - center_y  # Invert Y-axis to match standard cartesian coordinates

    if relative_x < -15:  # Object is to the left of the center
        print(f"{color_name} object detected at relative coordinates: ({relative_x}, {relative_y}). Turning left.")
        return "fl"
    elif relative_x > 15:  # Object is to the right of the center
        print(f"{color_name} object detected at relative coordinates: ({relative_x}, {relative_y}). Turning right.")
        return "fr"
    else:
        # Object is close to the center
        print(f"{color_name} object detected at relative coordinates: ({relative_x}, {relative_y}). Keeping centered.")
        return "f"


def main():
    red_ranges, pink_range, white_range = get_hsv_ranges()
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
        frame_center_x = frame_width // 2

        # Convert frame to HSV color space
        img_hsv = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)

        # Create masks for red, pink, and white
        red_mask, pink_mask, white_mask = create_combined_mask(img_hsv, red_ranges, pink_range, white_range)

        # Detect and draw circles for red
        red_center_x, red_center_y = detect_and_draw_circles(video, red_mask, "Red")

        # Detect center for pink objects
        pink_center_x, pink_center_y = detect_pink_center(video, pink_mask)

        # Detect and count white dots in the specified range
        detect_white_dots(video, white_mask, frame_center_x, frame_width_tolerance=10)

        # Process center positions for red and pink
        process_center_position(red_center_x, red_center_y, frame_width, frame_height, "Red")
        process_center_position(pink_center_x, pink_center_y, frame_width, frame_height, "Pink")

        # Display the video feed and masks
        combined_mask = red_mask | pink_mask | white_mask
        cv2.imshow("Mask Image", combined_mask)
        cv2.imshow("Video Feed", video)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


import RPi.GPIO as GPIO          
from time import sleep


# motor forwards-backwrds
in1 = 24
in2 = 23

# motor clockwise-anti
in3 = 21
in4 = 22

# speed of motor
en = 25 

# motordirection
temp1=1 


# GPIO Setup 
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(en)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop fr-forwardright br-backwardright fl-forwardleft bl-backwardleft f-forward b-backward l-low m-medium h-high e-exit")
print("\n")     

while(1):

    x=input()
    # motor1 forward-backward
    if x=='r':
        print("run")
        if(temp1==1):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)    
            print("forward")
            x='z'
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)  
            print("backward")
            x='z'

    # motor-stop 
    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)  
        x='z'

    # motor forward-right fr
    elif x=='fr':
        print("forwardright")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)      
        temp1=1
        x='z'

    # motor forward-left fl
    elif x=='fl':
        print("forwardleft")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)      
        temp1=1
        x='z'

    # motor backward-left bl
    elif x=='bl':
        print("backwardleft")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)      
        temp1=0
        x='z'

    # motor backward-right br
    elif x=='br':
        print("backwardright")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)      
        temp1=0
        x='z'

    # motor forward
    elif x=='f':
        print("forward1")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)   
        temp1=1
        x='z'

    # motor backward
    elif x=='b':
        print("forward1")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)   
        temp1=0
        x='z' 

    # # motor-1-forward
    # elif x=='f1':
    #     print("forward1")
    #     GPIO.output(in1,GPIO.HIGH)
    #     GPIO.output(in2,GPIO.LOW)
    #     temp1=1
    #     x='z'

    # # motor-2-forward
    # elif x=='f2':
    #     print("forward2")
    #     GPIO.output(in3,GPIO.HIGH)
    #     GPIO.output(in4,GPIO.LOW)
    #     temp1=1
    #     x='z'
        
    # motor-1-backward
    # elif x=='b1':
    #     print("backward")
    #     GPIO.output(in1,GPIO.LOW)
    #     GPIO.output(in2,GPIO.HIGH)
    #     temp1=0
    #     x='z'

    # motor-2-backward
    # elif x=='b2':
    #     print("backward")
    #     GPIO.output(in1,GPIO.LOW)
    #     GPIO.output(in2,GPIO.HIGH)
    #     temp1=0
    #     x='z'
    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")