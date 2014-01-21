#!/usr/bin/env python2

import os
import time
import sys

from flask import Flask, Response, render_template

# Tratamiento de imagenes
import cv2
from PIL import Image
from cStringIO import StringIO

PUERTO_WEB = 5000
ANCHO, ALTO = 640, 480
RETARDO = 0.001

capture = None



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('cam.html',
                            camara_url='http://127.0.0.1:5000/stream')

mjpeg_content_type = 'multipart/x-mixed-replace; boundary=--jpgboundary'


@app.route('/stream')
def cam():
    def camara_stream():
        global capture
        capture = cv2.VideoCapture(0)
        capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        capture.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.2)

        try:
            while True:
                rc, img = capture.read()
                if not rc:
                    continue
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                jpg = Image.fromarray(imgRGB)
                tmpfp = StringIO()
                jpg.save(tmpfp, 'JPEG')

                tmpfp.seek(0, os.SEEK_END)
                length = tmpfp.tell()
                tmpfp.seek(0)

                yield '--jpgboundary\r\n'
                yield 'Content-length: image/jpeg\r\n'
                yield 'Content-length: %d\r\n' % tmpfp.tell()
                yield '\r\n'
                yield '%s\r\n\r\n' % tmpfp.getvalue()
                del tmpfp  # Performance?
                time.sleep(RETARDO)

        except Exception as e:
            print e
        finally:
            capture.release()

    return Response(camara_stream(), content_type=mjpeg_content_type)


if __name__ == '__main__':
    app.run(debug=True, port=PUERTO_WEB)
