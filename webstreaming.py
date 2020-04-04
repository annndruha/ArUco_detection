# Script to run local web server with video streaming
# Also, recorded video saved to videos folder
# Marakulin Andrey @annndruha
# 2020
import cv2
import numpy as np
import time
import datetime
from flask import Flask, Response, redirect, request, url_for, render_template
from imutils.video import VideoStream

vs = VideoStream(src=0).start()
app = Flask(__name__)
message = ''

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/text_stream')
def text_stream():
    if request.headers.get('accept') == 'text/event-stream':
        def generate_text():
            while True:
                s = str(datetime.datetime.strftime(
                            datetime.datetime.now(
                            datetime.timezone(
                            datetime.timedelta(hours = 3))),'%Y.%m.%d  %H:%M:%S'))
                if message == '':
                    yield "data: %s\n\n" % (s,)
                else:
                    yield "data: %s\n\n" % (message,)
                time.sleep(.1)
        return Response(generate_text(), content_type='text/event-stream')


hight, wight, _ = vs.read().shape
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
timestamp = time.strftime("%H.%M.%S", time.gmtime(time.time()))
name = 'videos/out_%s.avi' % timestamp
print("Start at %s" % timestamp)

@app.route("/video_feed")
def video_feed():
    def video_generate():
        global vs
        global message
        try:
            out = cv2.VideoWriter(name, fourcc, 12.0, (wight,hight))
            while True:
                outputFrame = vs.read() # If need more functionality: move this two line to another thread
                (flag, encodedImage) = cv2.imencode(".jpg", outputFrame) # and update global frame and read it in video_generate func.
                out.write(outputFrame)
                time.sleep(0.08)
                message = ''
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
                
        except cv2.error as err:
            out.release()
            vs.stop()
            message = 'Camera unplugged.'
            vs = VideoStream(src=0).start()
            time.sleep(1)
            

    return Response(video_generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 