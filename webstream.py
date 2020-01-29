# Video streaming
# @annndruha
# 2020

import cv2
import os
from flask import Response
from flask import Flask
from flask import render_template
from flask import jsonify, request
from imutils.video import VideoStream

import time
import datetime
import argparse

vs = VideoStream(src=1).start()
app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    def video_generate():
        while True:
            outputFrame = vs.read() # If need more functionality: move this two line to another thread
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame) # and update global frame and read it in video_generate func.
            time.sleep(0.04)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
    return Response(video_generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/meta_info")
def meta_info():
    def meta_generate():
        while True:
            s = "["+str(datetime.datetime.strftime(
                        datetime.datetime.now(
                        datetime.timezone(
                        datetime.timedelta(hours = 3))),'%Y.%m.%d %H:%M:%S'))+"]"
            yield s
            time.sleep(1)
    return Response(meta_generate(), mimetype = "text/plain")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True, use_reloader=False)
    vs.stop()