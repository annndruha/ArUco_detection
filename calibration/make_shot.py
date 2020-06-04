# Use to make a camera shot by press 's'

import cv2
import numpy as np
import time
import os

cap = cv2.VideoCapture(1)
def make_shot(frame):
    if not (os.path.exists('images')): os.mkdir('images')
    timestamp = time.strftime("%H.%M.%S", time.gmtime(time.time()))
    cv2.imwrite(f"images/image_{timestamp}.png", frame)
    print(f'Image save images/image_{timestamp}.png')

while True:
    ret, frame = cap.read()

    cv2.imshow('Camera', frame)
    c = cv2.waitKey(2)
    if c & 0xFF == ord('q'):
        break
    if c & 0xFF == ord(' '):
        time.sleep(2)
        make_shot(frame)
    if c & 0xFF == ord('s'):
        make_shot(frame)