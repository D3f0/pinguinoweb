# -*- coding: utf-8 -*-

from pynguino import PinguinoProcessing
from datetime import datetime
p = PinguinoProcessing()
p.RecursiveConect()

pote = 13
p.pinMode(pote, "input")

import time


# Tratado del puerto serial
# pinguino=serial.Serial("/dev/ttyACM0")

with open('archivo.txt', 'w') as arch:

    try:
        while True:
            dato = str(p.analogRead(pote))
            fecha = datetime.now()
            print dato
            arch.write("%s,%s\n" % (fecha.strftime('%H:%M:%S %d-%m-%Y'), dato))
            time.sleep(1)
    except KeyboardInterrupt:
        print "Cerrando archivo"

