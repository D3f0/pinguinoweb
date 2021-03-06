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
import random
import werkzeug.serving



gevent.monkey.patch_all()


from flask import Flask, request, Response, render_template


app = Flask(__name__)
app.debug = True
app.context = zmq.Context(1)

DIRECCION_ENTRADA = 'tcp://127.0.0.1:5555'
DIRECCION_SALIDA = 'inproc://queue'


@app.route('/')
def index():
    '''Página principal desde donde se accede al resto de las páginas'''
    return render_template('index.html')

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


def generador_de_eventos():
    '''Una función que envía acutalizaciones usando el protocolo de
    eventos emitidos por el servidor (SSE). La directiva yield retorna
    un valor, pero la función conserva su estado ante cada llamada, por
    eso está rodeada de un while True'''
    sock = app.context.socket(zmq.SUB)
    sock.connect(DIRECCION_SALIDA)
    sock.setsockopt(zmq.SUBSCRIBE, "")
    while True:
        data = sock.recv()
        # Yield retorna un valor pero guarda estado de una función
        yield 'data: %s\n\n' % data


@app.route('/datos_tiempo_real/')
def sse_request():
    '''URL donde se publican los eventos'''
    return Response(generador_de_eventos(), mimetype='text/event-stream')


def genera_datos():
    '''Función que genera una onda senoidal tomando el clock
    de la PC'''
    sock = app.context.socket(zmq.PUB)
    sock.connect(DIRECCION_ENTRADA)

    diferencia_horaria = 3 * 60 * 60  # horas minutos segundos

    while True:
        gevent.sleep(.50)

        x = (time.time() * 1000) #+ diferencia_horaria
        #y = 2.5 * (1 + math.sin(x / 500))
        y = random.randrange(1,1000)/float(100)
        sock.send(json.dumps(dict(x=x, y=y)))


@app.route('/plot/')
def page():
    '''Dibujado de curvas en tiempo real'''
    return render_template('plot_sse.html', )


@app.route('/analog/')
def slider():
    '''Visualización de entradas analógicas'''
    return render_template('analog.html')


@app.route('/nvd3_plot/')
def nvd3_plot():
    '''Uses example take from http://jsfiddle.net/BjRLy/133/'''
    return render_template('nvd3_plot.html')

@app.route('/nvd3_plot_sse/')
def nvd3_plot_sse():
    '''Utiliza el código de plot de NVD3 pero con fuente
    de eventos SSE'''
    return render_template('nvd3_plot_sse.html')


@werkzeug.serving.run_with_reloader
def main():
    '''Función mainl del programa'''
    host, port = '0.0.0.0', 8080  # 0.0.0.0 significa todas las conexiones
                                  # (inalámbricas, cableadas, loopback) que
                                  # posea la computadora.
                                  # 8080 es el puerto
    print "Running server at {host}:{port}".format(host=host, port=port)

    gevent.spawn(retransmisor)
    gevent.spawn(genera_datos)
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()
    print "hola"

    #http_server.serve_forever()


if __name__ == '__main__':
    sys.exit(main())
