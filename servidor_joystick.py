# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from pynguino import PinguinoProcessing
from time import sleep as delay

# Comunicación y setup con Pingüino PIC18F4550
pinguino = PinguinoProcessing()
pinguino.RecursiveConect()

pote = 13

for pin in range(8):
    pinguino.pinMode(pin, "output")
    pinguino.digitalWrite(pin, 0)

def puertoB(A,B,C,D,E,F,G,H):
	pinguino.digitalWrite(0,A)		#digitalWrite(pin,estado)
	pinguino.digitalWrite(1,B)
	pinguino.digitalWrite(2,C)
	pinguino.digitalWrite(3,D)
	pinguino.digitalWrite(4,E)
	pinguino.digitalWrite(5,F)
	pinguino.digitalWrite(6,G)
	pinguino.digitalWrite(7,H)

# Aplicacion web
app = Flask(__name__)

# Crear página web que está en "inicio"
@app.route("/dato")
def dato():
    """Obtiene el dato del pin 13"""
    return str(pinguino.analogRead(pote))


@app.route('/medidor')
def medidor():
    """Esta pagina usa un medidor con aguja"""
    return render_template('medidor.html')

@app.route("/joystick")
def joystick():
    return render_template('joystick.html')

@app.route("/secuencial")
def secuencial():
    return render_template('secuencial.html')

@app.route("/motorPAP")
def motorPAP():
    return render_template('MotorPasoaPaso.html')


# Acciones a realizar con la placa pingüino.
@app.route('/mi_motorPAP', methods=['POST'])
def mi_motorPAP():
    tiempo=0.02		#Definición de una variable de tiempo en segundos
    pin = int(request.form['pin'])

    if pin == 0:
		puertoB(1,0,0,0,0,0,0,0)
		delay(tiempo)
		puertoB(0,1,0,0,0,0,0,0)
		delay(tiempo)
		puertoB(0,0,1,0,0,0,0,0)
		delay(tiempo)
		puertoB(0,0,0,1,0,0,0,0)
		delay(tiempo)

    if pin == 1:
		puertoB(0,0,0,1,0,0,0,0)
		delay(tiempo)
		puertoB(0,0,1,0,0,0,0,0)
		delay(tiempo)
		puertoB(0,1,0,0,0,0,0,0)
		delay(tiempo)
		puertoB(1,0,0,0,0,0,0,0)
		delay(tiempo)
			
    puertoB(0,0,0,0,0,0,0,0)
    return ""



@app.route('/mi_secuencial', methods=['POST'])
def mi_secuencial():
    tiempo=0.05		#Definición de una variable de tiempo en segundos
    tiempo2=0.1				
    pin = int(request.form['pin'])

    if pin == 0:
		for i in range(10):
			puertoB(1,0,0,0,0,0,0,0)
			delay(tiempo)
			puertoB(0,1,0,0,0,0,0,0)
			delay(tiempo)
			puertoB(0,0,1,0,0,0,0,0)
			delay(tiempo)
			puertoB(0,0,0,1,0,0,0,0)
			delay(tiempo)
			puertoB(0,0,0,0,1,0,0,0)
			delay(tiempo)
			puertoB(0,0,0,0,0,1,0,0)
			delay(tiempo)
			puertoB(0,0,0,0,0,0,1,0)
			delay(tiempo)
			puertoB(0,0,0,0,0,0,0,1)
			delay(tiempo)

    if pin == 1:
		for i in range(10):
			puertoB(1,0,0,0,0,0,0,0)
			delay(tiempo)
			puertoB(1,1,0,0,0,0,0,0)
			delay(tiempo)
			puertoB(1,1,1,0,0,0,0,0)
			delay(tiempo)
			puertoB(1,1,1,1,0,0,0,0)
			delay(tiempo)
			puertoB(1,1,1,1,1,0,0,0)
			delay(tiempo)
			puertoB(1,1,1,1,1,1,0,0)
			delay(tiempo)
			puertoB(1,1,1,1,1,1,1,0)
			delay(tiempo)
			puertoB(1,1,1,1,1,1,1,1)
			delay(tiempo)

    if pin == 2:
		for i in range(10):
			puertoB(1,1,1,1,1,1,1,1)
			delay(tiempo)
			puertoB(0,1,1,1,1,1,1,1)
			delay(tiempo)
			puertoB(0,0,1,1,1,1,1,1)
			delay(tiempo)
			puertoB(0,0,0,1,1,1,1,1)
			delay(tiempo)
			puertoB(0,0,0,0,1,1,1,1)
			delay(tiempo)
			puertoB(0,0,0,0,0,1,1,1)
			delay(tiempo)
			puertoB(0,0,0,0,0,0,1,1)
			delay(tiempo)
			puertoB(0,0,0,0,0,0,0,1)
			delay(tiempo)

    if pin == 3:
		for i in range(10):
			puertoB(1,0,0,0,0,0,0,1)
			delay(tiempo)
			puertoB(0,1,0,0,0,0,1,0)
			delay(tiempo)
			puertoB(0,0,1,0,0,1,0,0)
			delay(tiempo)
			puertoB(0,0,0,1,1,0,0,0)
			delay(tiempo)

    if pin == 4:
		for i in range(10):
			puertoB(1,1,1,1,0,0,0,0)
			delay(tiempo2)
			puertoB(0,0,0,0,1,1,1,1)
			delay(tiempo2)
    
    puertoB(0,0,0,0,0,0,0,0)
    return ""


@app.route('/mi_joystick', methods=['POST'])
def mi_joystick():
    pin = int(request.form['pin'])
    if request.form['pulsado'] == 'true':
		if pin == 0:
	    		pinguino.digitalWrite(0, 1)
	    		pinguino.digitalWrite(1, 0)
	    		pinguino.digitalWrite(2, 0)
	    		pinguino.digitalWrite(3, 1)

		if pin == 1:
	    		pinguino.digitalWrite(0, 0)
	    		pinguino.digitalWrite(1, 1)
	    		pinguino.digitalWrite(2, 1)
	    		pinguino.digitalWrite(3, 0)

		if pin == 2:
	    		pinguino.digitalWrite(0, 1)
	    		pinguino.digitalWrite(1, 0)
	    		pinguino.digitalWrite(2, 1)
	    		pinguino.digitalWrite(3, 0)

		if pin == 3:
	    		pinguino.digitalWrite(0, 0)
	    		pinguino.digitalWrite(1, 1)
	    		pinguino.digitalWrite(2, 0)
	    		pinguino.digitalWrite(3, 1)

		if pin == 4:
	    		pinguino.digitalWrite(0, 0)
	    		pinguino.digitalWrite(1, 0)
	    		pinguino.digitalWrite(2, 0)
	    		pinguino.digitalWrite(3, 0)
    else:
	    pinguino.digitalWrite(0, 0)
	    pinguino.digitalWrite(1, 0)
	    pinguino.digitalWrite(2, 0)
	    pinguino.digitalWrite(3, 0)
    return ""


if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0')
