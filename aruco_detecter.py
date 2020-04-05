# Aruco markers detector from camera stream
# Marakulin Andrey @annndruha
# 2020
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters =  cv2.aruco.DetectorParameters_create()
text_font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    # Read frame from camera
    ret, frame = cap.read()

    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    # Fix a opencv bug with int64
    markerCornersArr = np.int32(np.array(markerCorners))

    if len(markerCorners)>0: # If markers found markers
        # Make a border above marker
        new_frame = cv2.polylines(frame, markerCornersArr, True, color = (0,255,0), thickness = 2)

        # Draw a markerID
        for i, id in enumerate(markerIds):
            str_id = str(id[0])
            cors = markerCornersArr[i][0][0]
            cors=tuple([int(cors[0]), int(cors[1])])

            new_frame = cv2.putText(new_frame, str_id, cors, text_font, fontScale= 1, color =(0, 0, 255), thickness = 1)
    else:
        new_frame = frame

    cv2.imshow('Find markers', new_frame)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break