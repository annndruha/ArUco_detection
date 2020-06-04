import cv2
import os
import numpy as np
import time
import datetime
from flask import Flask, Response, redirect, request, url_for, render_template
from imutils.video import VideoStream
import cam_pos_detector as det

vs = VideoStream(src=0).start()
app = Flask(__name__)
message = ''

def get_time_str():
    dt = datetime.timedelta(hours = 3)
    tz =datetime.timezone(dt)
    now =datetime.datetime.now(tz)
    return str(datetime.datetime.strftime(now,'%Y.%m.%d  %H:%M:%S'))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/text_stream')
def text_stream():
    if request.headers.get('accept') == 'text/event-stream':
        def generate_text():
            while True:
                if message == '':
                    s = get_time_str()
                    yield "data: %s\n\n" % (s,)
                else:
                    yield "data: %s\n\n" % (message,)
                time.sleep(.1)
        return Response(generate_text(), content_type='text/event-stream')


hight, wight, _ = vs.read().shape
print("===Camera resolution: %sx%s" % (str(hight), str(wight)))
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
timestamp = time.strftime("%H.%M.%S", time.gmtime(time.time()))
if not (os.path.exists('videos')): os.mkdir('videos')
name = 'videos/out_%s.avi' % timestamp
print("===Stream start at %s on localhost:5000\n===" % timestamp)

@app.route("/video_feed")
def video_feed():
    def video_generate():
        global vs
        global message
        try:
            out = cv2.VideoWriter(name, fourcc, 12.0, (wight,hight))
            while True:
                outputFrame = vs.read()
                x, y, z, dst, frame = det.findPosition(outputFrame)
                if dst is not None:
                    message = f'x= {str(x)[:5] if x<0 else str(x)[:4]} y= {str(y)[:5] if x<0 else str(y)[:4]} z= {str(z)[:5] if x<0 else str(z)[:4]} dst= {str(dst)[:4]}'
                else:
                    message = 'x= ---- y= ---- z= ---- distance= ----'
                if frame is not None: outputFrame = frame
                
                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
                out.write(outputFrame)
                time.sleep(0.08)
                
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
                
        except cv2.error as err:
            # This dosn't work. Need to fix
            out.release()
            vs.stop()
            message = 'Camera unplugged.'
            vs = VideoStream(src=0).start()
            time.sleep(1)
            

    return Response(video_generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 