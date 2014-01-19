#!/usr/bin/python2
# -*- coding: utf-8 -*-

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
import sys
import zmq.green as zmq
import time
import math
import json
import werkzeug.serving


gevent.monkey.patch_all()


from flask import Flask, request, Response, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("d3/semaforo.html")


@werkzeug.serving.run_with_reloader
def runserver(host='', port=8080):
    app.debug = True

    ws = WSGIServer((host, port), app)
    ws.serve_forever()


def main():
    runserver()

if __name__ == '__main__':
    main()
