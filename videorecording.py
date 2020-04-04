import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

fourcc = cv2.VideoWriter_fourcc(*'MPEG')#MP4V

VIDEO_LEN_SEC = 20
NUMBER_OF_VIDEO = 3
print("===Script start")
for m in range(NUMBER_OF_VIDEO):
    t = time.time()
    timestamp = time.strftime("%H.%M.%S", time.gmtime(t))
    name = f'videos/output_{timestamp}.avi'#.mp4
    print(f"{timestamp}: Video number = {m+1}/{NUMBER_OF_VIDEO}")

    out = cv2.VideoWriter(name, fourcc, 20.0, (640,480))
    i = 0
    while time.time()< t + VIDEO_LEN_SEC:
        framestart = time.time()
        i+=1
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame', frame)
        if (framestart+0.05)<time.time():
            time.sleep(time.time()-(framestart+0.05))
        #c = cv2.waitKey(2)
        #if c & 0xFF == ord('q'):
        #    break
    print(i)
    i=0
    out.release()

cap.release()
cv2.destroyAllWindows()
print("===Script end")