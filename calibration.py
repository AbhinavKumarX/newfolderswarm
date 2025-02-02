import cv2
import numpy as np
import glob

# Termination criteria for subpixel corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
# Change the size depending on the checkerboard you are using
objp = np.zeros((6*7, 3), np.float32)  # For a 7x6 checkerboard
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane

# Load images for calibration (use your actual path)
images = glob.glob('calibration_images/*.jpg')  # Path to your checkerboard images

# Read the first image to get its dimensions
img = cv2.imread(images[0])  # Just read one image to get the dimensions
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Loop over all the images
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

    if ret:
        objpoints.append(objp)  # Add object points
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)  # Refine corner locations
        imgpoints.append(corners2)  # Add image points

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
        cv2.imshow('Chessboard', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()  # Close the image window

# Perform camera calibration to get camera matrix and distortion coefficients
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save the calibration results for later use
np.savez('camera_calibration.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

# Output the results
print("Camera matrix:")
print(mtx)
print("Distortion coefficients:")
print(dist)