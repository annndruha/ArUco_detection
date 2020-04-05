import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'MPEG')

VIDEO_LEN_SEC = 60
NUMBER_OF_VIDEO = 3
print("===Script start")
for m in range(NUMBER_OF_VIDEO):
    t = time.time()
    timestamp = time.strftime("%H.%M.%S", time.gmtime(t))
    name = f'videos/output_{timestamp}.avi'
    print(f"{timestamp}: Video number = {m+1}/{NUMBER_OF_VIDEO}")

    out = cv2.VideoWriter(name, fourcc, 20.0, (640,480))

    while time.time()< t + VIDEO_LEN_SEC:
        ret, frame = cap.read()
        out.write(frame) # Encoding takes different time. Need to find way to stable .avi FPS
        cv2.imshow('frame', frame)

        c = cv2.waitKey(2)
        if c & 0xFF == ord('q'):
            break

    out.release()

cap.release()
cv2.destroyAllWindows()
print("===Script end")