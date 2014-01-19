# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from pynguino import PinguinoProcessing
import webbrowser
import thread
import time


host = '0.0.0.0'
port = 5000


app = Flask(__name__)
pinguino = None


def configurar_pinguino():
    global pinguino
    pinguino = PinguinoProcessing()
    pinguino.RecursiveConect()
    pinguino.pinMode(11,"output")  #pinMode(pin,"output" ó "input")
    pinguino.analogWrite(11, 0)



@app.route('/')
def index():
    return render_template('knob.html')


@app.route('/analog_write/<int:pin>/<int:valor>/')
def analog_write(pin, valor):
    pinguino.analogWrite(pin, valor)
    return ""


def lanzar_navegador():
    webbrowser.open('http://localhost:%d' % port)

if __name__ == '__main__':
    configurar_pinguino()
    thread.start_new_thread(lanzar_navegador, () )
    app.run(debug=True, host=host, port=port)

