'''class ref:
       def __init__(self, obj): self.obj = obj
       def get(self):    return self.obj
       def set(self, obj):      self.obj = obj

a = ref([1, 2])
b = a
c = ref(a.get())
print (a.get())  # => [1, 2]
print (b.get())  # => [1, 2]
print (c.get())  # => [1, 2]
a.set(4)
print (a.get())  # => 4
print (b.get())  # => 4
print (c.get())  # => [1, 2]

import re

pattern = r'(\$t[0-9]+)'
match = re.match(pattern,"$t245$t555")
if match:
       print(match.group())


index = 0
def sumar():
       global index
       index = index +1

sumar()
sumar()
sumar()

def otro():
       sumar()
otro()
print(index)
'''

'''class retornarsuma:
       def __init__(self,operador1, operador2):
              self.op1 = operador1
              self.op2 = operador2

class numero:
       def __init__(self,valor):
              self.valor= valor

def procesar(instruccion):
       op1 = obtenerNumero(instruccion.op1)
       op2 = obtenerNumero(instruccion.op2)
       return op1+op2

def obtenerNumero(num):
       return num.valor

numero1 = numero(3)
numero4 = numero(5)

operacion = procesar(retornarsuma(numero1, numero4))
print(operacion)'''

'''import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from PyQt5 import Qt

class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Return:
            print("pressed")
        event.accept()



app = QApplication([])
p = Principal()
p.show()
app.exec_()'''

'''import time
contador = 0
while contador <= 100:
       time.sleep(1)
       contador+=1
       print(contador)
print("TIEMPO EXCEDIDO DE LECTURA")'''

print(1 and 0)