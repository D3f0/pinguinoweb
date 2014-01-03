#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
import sys
import zmq.green as zmq
import time
import math
import json


gevent.monkey.patch_all()


from flask import Flask, request, Response, render_template


app = Flask(__name__)
app.debug = True
app.context = zmq.Context(1)

DIRECCION_ENTRADA = 'tcp://127.0.0.1:5555'
DIRECCION_SALIDA = 'inproc://queue'


def retransmisor(dir_entrada=DIRECCION_ENTRADA,
                 dir_salida=DIRECCION_SALIDA):
    '''Utiliza un dipositivo forwareder para retransmitir mensajes
    desde un extremo subscriptor, hacia una extremo emisor. Pueden
    existir múltiples emisores y múltiples receptores conectados
    al dispositivo retransmisor.
    Ver https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/devices/forwarder.html
    '''
    try:
        entrada = app.context.socket(zmq.SUB)
        entrada.bind(dir_entrada)
        entrada.setsockopt(zmq.SUBSCRIBE, '')

        salida = app.context.socket(zmq.PUB)
        salida.bind(dir_salida)
        print "Launching device"
        zmq.device(zmq.FORWARDER, entrada, salida)
    except Exception, e:
        print e
        raise e
    finally:
        entrada.close()
        salida.close()
        app.context.term()


def event_stream():
    sock = app.context.socket(zmq.SUB)
    sock.connect(DIRECCION_SALIDA)
    sock.setsockopt(zmq.SUBSCRIBE, "")
    while True:
        data = sock.recv()
        yield 'data: %s\n\n' % data


@app.route('/my_event_source')
def sse_request():
    return Response(event_stream(), mimetype='text/event-stream')


def sender():
    sock = app.context.socket(zmq.PUB)
    sock.connect(DIRECCION_ENTRADA)
    count = 0
    while True:
        gevent.sleep(0.01)
        x = time.time() * 1000
        y = 2.5 * (1 + math.sin(x / 500))
        sock.send(json.dumps(dict(x=x, y=y)))
        count += 1


@app.route('/')
def page():
    return render_template('sse.html')


def main():
    host, port = '0.0.0.0', 8080
    print "Running server at {host}:{port}".format(host=host, port=port)

    gevent.spawn(retransmisor)
    gevent.spawn(sender)
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()


    #http_server.serve_forever()


if __name__ == '__main__':
    sys.exit(main())
