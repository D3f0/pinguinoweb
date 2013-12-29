# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from random import randint
from pynguino import PinguinoProcessing

p = PinguinoProcessing()
p.RecursiveConect()

pote = 13
p.pinMode(pote, "input")

for pin in range(8):
    p.pinMode(pin, "output")
    p.digitalWrite(pin, 0)
# Tratado del puerto serial
# pinguino=serial.Serial("/dev/ttyACM0")


# Aplicacion web
app = Flask(__name__)


# Pagina que está en "incio"
@app.route("/")
def hello():
    return render_template('base.html')

@app.route("/dato")
def dato():
    """Obtiene el dato del pin 13"""
    return str(p.analogRead(pote))


@app.route('/medidor')
def medidor():
    """Esta pagina usa un medidor con aguja"""
    return render_template('medidor.html')


@app.route("/botones")
def botones():
    return render_template('botones.html')

@app.route('/cambiar_led', methods=['POST'])
def cambiar_led():
    pin = int(request.form['pin'])
    if request.form['pulsado'] == 'true':
        estado = 1
    else:
        estado = 0
    print "Estableciendo", pin, estado
    p.digitalWrite(pin, estado)
    return ""

if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0')
