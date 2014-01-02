#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
import sys
import zmq.green as zmq


gevent.monkey.patch_all()


from flask import Flask, request, Response, render_template

#import zmq
#from zmq import devices

# print "ZMQ"


app = Flask(__name__)
app.debug = True


def retransmisor(context,
                 dir_entrada='tcp://*:5555',
                 dir_salida='tcp://*:5566'):
    '''Utiliza un dipositivo forwareder para retransmitir mensajes
    desde un extremo subscriptor, hacia una extremo emisor. Pueden
    existir múltiples emisores y múltiples receptores conectados
    al dispositivo retransmisor.
    Ver https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/devices/forwarder.html
    '''
    try:
        entrada = context.socket(zmq.SUB)
        entrada.bind(dir_entrada)
        entrada.setsockopt(zmq.SUBSCRIBE, '')

        salida = context.socket(zmq.SUB)
        salida.bind(dir_salida)
        print "Launching device"
        print
        zmq.device(zmq.FORWARDER, entrada, salida)
    except Exception, e:
        print e
        raise e
    finally:
        entrada.close()
        salida.close()
        context.term()


def event_stream():
    count = 0
    while True:
        gevent.sleep(2)
        yield 'data: %s\n\n' % count
        count += 1


@app.route('/my_event_source')
def sse_request():
    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/')
def page():
    return render_template('sse.html')


def main():
    host, port = '0.0.0.0', 8080
    print "Running server at {host}:{port}".format(host=host, port=port)

    context = zmq.Context(1)
    gevent.spawn(retransmisor, context)
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()

    #http_server.serve_forever()


if __name__ == '__main__':
    main()
