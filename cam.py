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
VELOCIDAD = 0.0

capture = None



app = Flask(__name__)


@app.route('/')
@add_headers(a=1, b=2)
def index():
    return render_template('cam.html',
                            camara_url='http://127.0.0.1:5000/camara/320/240/')

mjpeg_content_type = 'multipart/x-mixed-replace; boundary=--jpgboundary'


@app.route('/camara/<int:ancho>/<int:alto>/')
def cam(ancho, alto):
    def camara_stream():
        global capture
        capture = cv2.VideoCapture(0)
        capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, ancho)
        capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, alto)
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
                yield '--jpgboundary\r\n'
                yield 'Content-length: image/jpeg\r\n'
                tmpfp.seek(0, os.SEEK_END)
                yield 'Content-length: %d\r\n' % tmpfp.tell()
                yield '\r\n'
                tmpfp.seek(0)
                yield '%s\r\n\r\n' % tmpfp.getvalue()
                del tmpfp  # Performance?
                time.sleep(VELOCIDAD)

        except Exception as e:
            print e
        finally:
            capture.release()

    return Response(camara_stream(), content_type=mjpeg_content_type)


if __name__ == '__main__':
    app.run(debug=True, port=PUERTO_WEB)
