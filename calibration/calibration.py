# Script to find calibration coefficients (camera_matrix and dist_coeff)
# Input: Folder with images of Chessboard N*M, with different foreshortening, scale etc.
# Output: json file with two array variable
# Marakulin Andrey @annndruha
# 2020
import numpy as np
import cv2
import glob
import json

# INPUT:
images = glob.glob('images/*.png')
N = 7
M = 7
# =====

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((N*M,3), np.float32)
objp[:,:2] = np.mgrid[0:N,0:M].T.reshape(-1,2)

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

valid_images_used = 0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (N,M), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        valid_images_used +=1

        cv2.drawChessboardCorners(img, (N,M), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(800)
cv2.destroyAllWindows()

_, camera_matrix, dist_coeff, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(f'valid_images_used = {str(valid_images_used)}')

# OUTPUT:
data = {"camera_matrix": camera_matrix.tolist(), "dist_coeff": dist_coeff.tolist()}
with open("calibration_data.json", "w") as f:
    json.dump(data, f)