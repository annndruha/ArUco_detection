import numpy as np
import cv2
import time
import os

cap = cv2.VideoCapture(0)


VIDEO_LEN_SEC = 600

t = time.time()
timestamp = time.strftime("%H.%M.%S", time.gmtime(t))
if not (os.path.exists('videos')):
    os.mkdir('videos')
name = f'videos/output_{timestamp}.avi'

out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'MPEG'), 30.0, (640,480))
while time.time()< t + VIDEO_LEN_SEC:
    ret, frame = cap.read()
    out.write(frame) # Encoding takes different time. Need to find way to stable .avi FPS

    #cv2.imshow('frame', frame)
    #if cv2.waitKey(2) & 0xFF == ord('q'):
    #    break


out.release()
cap.release()
cv2.destroyAllWindows()