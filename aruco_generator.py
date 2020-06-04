import cv2
import numpy as np

MARKER_ID = 5
di = cv2.aruco.DICT_6X6_50

RESOLUTION = 200
markerImage = np.zeros((RESOLUTION, RESOLUTION), dtype=np.uint8)
markerImage = cv2.aruco.drawMarker(cv2.aruco.Dictionary_get(di), MARKER_ID, RESOLUTION, markerImage, 1)

cv2.imwrite(f"marker{MARKER_ID}.png", markerImage)