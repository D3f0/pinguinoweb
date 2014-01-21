#!/usr/bin/env python2

import sys, os, time, atexit


# Multitarea
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
# Comunicaciones
import zmq.green as zmq

# Web Server
from flask import Flask, Response, render_template

# Tratamiento de imagenes
import cv2
from PIL import Image
from cStringIO import StringIO
from multiprocessing import Process

# Debug
import werkzeug

gevent.monkey.patch_all()

PUERTO_WEB = 5000
ANCHO, ALTO = 640, 480
VELOCIDAD = 0.0


DIRECCION_PUBLICADOR = 'tcp://127.0.0.1:3344'

capture = None


def limpieza(captura):
    if captura is not None:
        try:
            captura.release()
        except Exception as e:
            print e


def camara_prductor():

    ancho, alto = 320, 240
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.bind(DIRECCION_PUBLICADOR)
    capture = cv2.VideoCapture(0)
    atexit.register((capture,))

    capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, ancho)
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, alto)
    capture.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.2)
    while True:
        rc, img = capture.read()
        if not rc:
            continue
        tmpfp = StringIO()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        tmpfp = StringIO()
        jpg.save(tmpfp, 'JPEG')
        tmpfp.seek(0, os.SEEK_END)
        length = tmpfp.tell()
        tmpfp.seek(0)
        output = (
            '--jpgboundary\r\n',
            'Content-type: image/jpeg\r\n',
            ('Content-length: %d\r\n' % length),
            '\r\n',
            tmpfp.read(),
            '\r\n\r\n'
        )

        socket.send(''.join(output))



app = Flask(__name__)
app.context = zmq.Context(1)

@app.route('/')
def index():
    return render_template('cam.html',
                            camara_url='http://127.0.0.1:5000/camara/')

mjpeg_content_type = 'multipart/x-mixed-replace; boundary=--jpgboundary'


@app.route('/camara/')
def cam():
    def camara_stream():
        try:
            socket = app.context.socket(zmq.SUB)
            socket.connect(DIRECCION_PUBLICADOR)
            socket.setsockopt(zmq.SUBSCRIBE, "")
            while True:
                data = socket.recv()
                yield data
        except Exception as e:
            import traceback as tb; print tb.format_exc()

    return Response(camara_stream(), content_type=mjpeg_content_type)

#@werkzeug.serving.run_with_reloader
def runserver(host='', port=PUERTO_WEB):
    app.debug = True

    ws = WSGIServer((host, port), app)
    ws.serve_forever()


if __name__ == '__main__':
    captura = Process(target=camara_prductor)
    captura.start()
    runserver()
