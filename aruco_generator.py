import cv2 as cv
import numpy as np

MARKER_ID = 42 # ID from 0 tp 1023

dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
markerImage = np.zeros((200, 200), dtype=np.uint8)
markerImage = cv.aruco.drawMarker(dictionary, MARKER_ID, 200, markerImage, 1)

cv.imwrite(f"marker{MARKER_ID}.png", markerImage)