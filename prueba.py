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
'''dic_principal = {}
lst_direcciones = [0,'nombre']
valor="Daniel"
indice = 0


def agregar(lst_direcciones, dic_principal,valor):
       temporal = dic_principal
       for x in range(len(lst_direcciones)):
              new_dic = {}
              if (x+1)==len(lst_direcciones):
                     temporal[lst_direcciones[x]]=valor
              else:
                     temporal[lst_direcciones[x]]=new_dic
              temporal=new_dic

agregar(lst_direcciones,dic_principal,"Carlos")
lst_direcciones = [1,'nombre']
agregar(lst_direcciones,dic_principal,"Andree")
lst_direcciones = [2,'nombre']
agregar(lst_direcciones,dic_principal,"Avalos")
lst_direcciones = [3,'nombre']
agregar(lst_direcciones,dic_principal,"Soto")

print(dic_principal)'''
import ply.yacc as yacc
import ply.lex as lex


reservadas = {
       'hola':'RESERVADA'
}

tokens = [
    'COMA',
    'ID'
] + list(reservadas.values())

t_COMA = r','

def t_ID(t):
     r'id[0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_error(t):
    #editar para agregar a una tabla
    print("Illegal character '%s'" % t.value[0])
    #agregarError('Lexico',"Caracter \'{0}\' ilegal".format(t.value[0]), t.lexer.lineno+1,find_column(t))
    t.lexer.skip(1)


stack = []

lexer = lex.lex()


def p_init(p):
       'init : instrucciones'
       print(p[1])

def p_instrucciones(p):
       'instrucciones  :   ID instruccionesP'
       p[2].insert(0,p[1])
       p[0] = p[2]

def p_instruccionesP(p):
       '''instruccionesP   :  COMA intruccion instruccionesP
       '''
       
       #print(find_column(p.slice[-1].token))
       p[3].insert(0,p[2])
       p[0] = p[3]

def p_instruccionesP2(p):
       'instruccionesP   :'
       p[0] = []
       
def p_instruccion(p):
       'intruccion   : ID'
       print(p.slice[1])
       p[0] = p[1]

def find_column(token):
       line_start = -1
       return (token.lexpos - line_start) + 1


parser = yacc.yacc()
input = ""
def parse(inpu) :
    global input
    global lexer
    lexer.lineno=0
    input = inpu
    return parser.parse(inpu)

parse("id,id2,id3")