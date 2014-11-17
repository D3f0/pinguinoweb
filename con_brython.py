# -*- coding: utf-8 -*-
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, request
from gevent import sleep, spawn_later
from datetime import datetime
import json
import random, os
import webbrowser

random.seed(os.getpid())


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('con_brython.html', title="Pruebas con Brython")


@app.route('/websocket')
def websocket():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            sleep(0.5)
            ahora = "%s" % datetime.now()
            dato = {
                'fecha': ahora,
                'led': random.randint(0, 8)
            }
            cadena = json.dumps(dato)
            ws.send(cadena)
    return

if __name__ == '__main__':
    print u"Lanzando servidor y un navegador 2 segundos más tarde"

    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    spawn_later(2, lambda : webbrowser.open('http://localhost:5000'))
    http_server.serve_forever()