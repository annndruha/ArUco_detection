# Find a coordinates of camera, relative to ArUco marker with known parameters
# Marakulin Andrey
# 2020
import cv2
import numpy as np
import json
import os

# Load camera parametrs
path = os.path.split(__file__)[0]
with open(path+'/calibration/calibration_data.json') as f:
    data = json.load(f)
    cameraMatrix, distCoeffs = np.array(data['camera_matrix']), np.array(data['dist_coeff'])

# Init ArUco Parameters
MARKER_FACE_LEN = 0.12 # meters
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters =  cv2.aruco.DetectorParameters_create()

def findPosition(frame):
    markerCorners, markerIds, _ = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(markerCorners, MARKER_FACE_LEN, cameraMatrix, distCoeffs)

    for i, id in enumerate(markerCorners):
        frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
        frame = cv2.aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec[i], tvec[i], 0.05)#0.08

    if len(markerCorners)>0:
        R, _ = cv2.Rodrigues(rvec[0])
        rotation_matrix = np.array(R)
        translation_matrix = np.array(tvec[0][0])
        cameraPose = (rotation_matrix.T).dot(-translation_matrix)
        x, y, z = cameraPose
        dst = np.linalg.norm(cameraPose)
        return (x,y,z,dst, frame)
    return None, None, None, None, None

if __name__=='__main__':
    # Open a camera
    cap = cv2.VideoCapture(1)
    while True:
        _, frame = cap.read()
        # Find markers corners and ids
        markerCorners, markerIds, _ = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        # Find rotation and translation vectors in camera coordinates system
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(markerCorners, MARKER_FACE_LEN, cameraMatrix, distCoeffs)

        for i, id in enumerate(markerCorners):
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
            frame = cv2.aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec[i], tvec[i], 0.08)

        # Translate to camera position Cartesian coordinate system and print it
        if len(markerCorners)>0:
            R, _ = cv2.Rodrigues(rvec[0])
            rotation_matrix = np.array(R)
            translation_matrix = np.array(tvec[0][0])
            cameraPose = (rotation_matrix.T).dot(-translation_matrix)
            x, y, z = cameraPose
            dst = np.linalg.norm(cameraPose)
            print(f'x= {str(x)[:5]} y= {str(y)[:5]} z= {str(z)[:5]} dst= {str(dst)[:5]}')

        # Show image
        cv2.imshow('Found markers', frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break