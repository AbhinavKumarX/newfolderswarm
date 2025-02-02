from balldetectandgoaldetect import process_center_position

def control_motor(command):
    """Controls the motor based on the given command."""
    if command == "fl":
        print("Motor: Turning left.")
    elif command == "fr":
        print("Motor: Turning right.")
    elif command == "f":
        print("Motor: Staying centered.")
    else:
        print("Motor: Invalid command.")

# Example usage in your application
# Replace these values with real-time inputs from your detection logic
center_x, center_y = 200, 240  # Example coordinates
frame_width, frame_height = 640, 480
command = process_center_position(center_x, center_y, frame_width, frame_height, "Red")
control_motor(command)