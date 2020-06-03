from enum import Enum

class Tipo(Enum):
    ENTERO = 1
    DECIMAL = 2
    STRING = 3
    CHAR = 4

class Tipo_Simbolo(Enum):
    TEMPORAL = 1
    ARREGLONUMERICO =2
    STRUCT = 3
    MAIN = 4
    ETIQUETA = 5
    PARAMETRO = 6
    RETORNO = 7
    SIMULADOR = 8
    PILA = 9
    PUNTERO = 10
    INVALIDO = 11

class  Tipo_Etiqueta(Enum):
    FUNCION = 1
    PROCEDIMIENTO = 2
    CONTROL = 3
    MAIN = 4
    VARIABLE = 5

#clase para simular un apuntador
class ref:
    def __init__(self, valor):
        self.val = valor
    def set(self, new_val):
        self.val = new_val
    def get(self):
        return self.val

class Simbolo:
    def _init_(self, tipo_etiqueta, *args):
        if tipo_etiqueta == Tipo_Etiqueta.VARIABLE:
            self.id = args[0]
            self.valor = ref(args[1])
            self.tipo = args[2]
            self.ambiente = args[3]
            self.etiqueta = Tipo_Etiqueta.VARIABLE

'''
Clase Tabla de Simbolo donde se almacenaran los  simbolos pertenecientes a recoleccion de datos de la primera pasada
    y posteriormente su ejecucion.
'''
class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}

    #Metodo para agregar un simbolo a la tabla de simbolos
    def add(self, simbolo):
        self.simbolos[simbolo.id] = simbolo
    #Metodo para obtener un simbolo teniendo su id
    def get(self, id):
        return self.simbolos[id]
    #Metodo para actualizar un simbolo
    def actualizar(self,simbolo):
        self.simbolos[simbolo.id] = simbolo
    #Metodo que indica si existe variable en la tabla de simbolos
    def existe(self, id):
        return id in self.simbolos
    #Metodo para referenciar una variable
    def referenciar(self, id, valor):
        self.simbolos[id].valor.set(valor)
    
    
