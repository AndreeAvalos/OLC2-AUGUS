from TablaSimbolos import Tipo_Etiqueta, Tipo_Simbolo
import re 
class Instruccion:
    ''' Clase implementada para poderla utilizarla como interfaz'''

class Main(Instruccion):
    def __init__(self, instrucciones, line, column):
        self.etiqueta = Tipo_Etiqueta.MAIN
        self.id = "main"
        self.sentencias = instrucciones
        self.tipo = Tipo_Simbolo.MAIN
        self.line = line
        self.column = column
        self.valor = None

class Etiqueta(Instruccion):
    def __init__(self, id, instrucciones, line, column):
        self.etiqueta = Tipo_Etiqueta.CONTROL
        self.id = id
        self.sentencias = instrucciones
        self.tipo = Tipo_Simbolo.ETIQUETA
        self.line = line
        self.column = column
        self.valor = None

class Asignacion(Instruccion):
    def __init__(self, id, valor, etiqueta, line, column):
        self.etiqueta = etiqueta
        #temporales
        pattern = r'(\$t[0-9]+)'
        match1 = re.match(pattern,id)
        #parametros
        pattern = r'(\$a[0-9]+)'
        match2 = re.match(pattern,id)
        #retornos
        pattern = r'(\$v[0-9]+)'
        match3 = re.match(pattern,id)
        #pila
        pattern = r'(\$s[0-9]+)'
        match4 = re.match(pattern,id)
        if match1: 
            self.tipo = Tipo_Simbolo.TEMPORAL
            self.id = match1.group()
        elif match2:            
            self.tipo = Tipo_Simbolo.PARAMETRO
            self.id = match2.group()
        elif match3:            
            self.tipo = Tipo_Simbolo.RETORNO
            self.id = match3.group()
        elif match4:            
            self.tipo = Tipo_Simbolo.PILA
            self.id = match4.group()
        elif id == "$ra":
            self.tipo = Tipo_Simbolo.SIMULADOR
            self.id = "$ra"
        elif id == "$sp":
            self.tipo = Tipo_Simbolo.PUNTERO
            self.id = "$sp"
        else:
            self.tipo = Tipo_Simbolo.INVALIDO
            self.id = id
        self.valor = valor
        self.line = line
        self.column = column
