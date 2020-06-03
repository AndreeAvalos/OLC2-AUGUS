from enum import Enum
from Instruccion import Instruccion

class OPERACION_LOGICA(Enum):
    AND = 1
    OR = 2
    NOT = 3


class OPERACION_RELACIONAL(Enum):
    MAYOR = 1
    MAYORQUE = 2
    MENOR = 3
    MENORQUE = 4
    IGUAL = 5
    DIFERENTE = 6

class OPERACION_NUMERICA(Enum):
    SUMA = 1
    RESTA = 2
    MULTIPLICACION = 3
    DIVISION = 4
    MODULAR = 5

class OperacionBinaria(Instruccion):
    def __init__(self, op1, op2, operacion, line, column):
        self.operadorIzq = op1
        self.operadorDer = op2
        self.operacion = operacion

class OperacionNumero(Instruccion):
    def __init__(self,num, line, column):
        self.val = num