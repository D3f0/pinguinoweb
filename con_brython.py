# -*- coding: utf-8 -*-
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, request
from gevent import sleep
from datetime import datetime
# from pynguino import PinguinoProcessing
# import webbrowser
# import thread
# import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('con_brython.html', title="Pruebas con Brython")


@app.route('/websocket')
def websocket():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            sleep(1)
            ws.send("%s" % datetime.now())
    return

if __name__ == '__main__':
    print "Lanzando servidor"
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()