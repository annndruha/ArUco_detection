import itertools
import time
import datetime
from flask import Flask, Response, redirect, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':

        def events():
            while True:
                s = str(datetime.datetime.strftime(
                            datetime.datetime.now(
                            datetime.timezone(
                            datetime.timedelta(hours = 3))),'%Y.%m.%d  %H:%M:%S'))
                yield "data: %s\n\n" % (s,)
                time.sleep(.1)

        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='index2.html'))

if __name__ == "__main__":
    app.run(host='localhost', port=80) 