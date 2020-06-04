# Aruco markers detector
# Marakulin Andrey @annndruha
# 2020
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters =  cv2.aruco.DetectorParameters_create()

while True:
    ret, frame = cap.read()

    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

    new_frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

    cv2.imshow('Found markers2', new_frame)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break