import ply.yacc as yacc
import ply.lex as lex
from Instruccion import *
from Operacion import *
import subprocess

index =0 

def cmd(commando):
    subprocess.run(commando, shell=True)


class Nodo:
    def __init__(self,nodoast,nodog):
        self.instruccion = nodoast
        self.nodo = nodog

class NodoG:
    def __init__(self,indic, nombre, childs = []):
        self.index = indic
        self.nombre = nombre
        self.childs= childs
    def add(self, child):
        self.childs.append(child)



def construirAST(nodo):
    try:
        file = open("ASPAscendente.dot", "w")
        file.write("digraph{ bgcolor = gray \n node[fontcolor = white, height = 0.5, color = white] \n [shape=box, style=filled, color=gray14] \n rankdir=UD \n edge[color=white, dir=fordware]\n")
        imprimirNodos(nodo,file)
        graficar(nodo,file)
        file.write("\n}")
    except:
        print("ERROR")
    finally:
        file.close()
        cmd("dot -Tpng ASPAscendente.dot -o ASPAscendente.png")

def imprimirNodos(nodo,file):
    file.write(str(nodo.index)+"[style = \"filled\" ; label = \""+nodo.nombre+"\"] \n")
    if nodo.childs != None:
        for child in nodo.childs:
            imprimirNodos(child, file)

def graficar(nodo,file):
    if nodo.childs != None:
        for child in nodo.childs:
            file.write(str(nodo.index)+"->"+str(child.index)+";\n")
            graficar(child,file)
    

reservadas = {
    #Tipos para castear
    'int': 'INTEGER',
    'float': 'FLOAT',
    'char': 'CHAR',
    'print': 'PRINT',
    'main': 'MAIN',
    'goto': 'GOTO',
    'unset': 'UNSET',
    'read': 'READ',
    'exit': 'EXIT',
    'if': 'IF',
    'abs': 'ABS',
    'xor': 'XOR',
    'array': 'ARRAY'
}

tokens = [
    'PYCOMA',
    'LLAVEIZQ',
    'LLAVEDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'IGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'DECIMAL',
    'ENTERO',
    'CARACTER',
    'CADENA',
    'ID',
    'MAS',
    'MENOS',
    'MULTIPLICACION',
    'DIVISION',
    'MODULAR',
    'NOT',
    'AND',
    'OR',
    'NOTBIT',
    'ANDBIT',
    'ORBIT',
    'XORBIT',
    'SHIFTIZQ',
    'SHIFTDER',
    'DOSPUNTOS',
    'VARIABLE'
] + list(reservadas.values())

t_PYCOMA = r';'
t_DOSPUNTOS = r':'
t_LLAVEIZQ =r'{'
t_LLAVEDER = r'}'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_IGUAL = r'='
t_IGUALIGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULAR = '%'
t_NOT = r'!'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOTBIT = r'~'
t_ANDBIT = r'&'
t_ORBIT = r'\|'
t_XORBIT = r'\^'
t_SHIFTIZQ = r'<<'
t_SHIFTDER = r'>>'

t_ignore = " \t"

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error: %d ", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        #editar
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_VARIABLE(t):
     r'\$[a-z][a-z]*[0-9]*'
     t.type = reservadas.get(t.value.lower(),'VARIABLE')
     return t


def t_CADENA(t):
    r'\'.*\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CARACTER(t):
    r'\'[a-zA-Z0-9]\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_COMENTARIO(t):
    r'\#.*\n'
    t.lexer.lineno += 1



def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    #editar para agregar a una tabla
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
'''
precedence = (
    ('left','XOR'),
    ('left','AND'),
    ('left','NOT'),
    ('left','IGUALIGUAL', 'DIFERENTE','MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO', 'MODULAR'),
    #('right','UMENOS'),
    )
'''

def getIndex():
    global index
    index = index+1
    return index

def p_init(p):
    'init : instrucciones'
    print('init : instrucciones; init = instruccion')
    nodo2 = NodoG(getIndex(),"init", [])
    for item in p[1].nodo:
        nodo2.add(item)
    p[0] = Nodo(p[1].instruccion, nodo2)

def p_instrucciones(p):
    ''' instrucciones : instrucciones instruccion '''
    p[1].instruccion.append(p[2].instruccion)
    p[1].nodo.append(p[2].nodo)
    nodo = NodoG(getIndex(),"instrucciones",p[1].nodo)
    p[0] = Nodo(p[1].instruccion,[nodo])
    print("instrucciones : instrucciones instruccion; {instrucciones2.append(instruccion); instrucciones = instrucciones2}")

        
def p_instrucciones2(p):
    ' instrucciones : instruccion '
    p[0]= Nodo([p[1].instruccion],[NodoG(getIndex(),"instruccion",[p[1].nodo])])
    print("instrucciones : instruccion; instrucciones = new lista; instrucciones.append(instruccion)")


def p_instruccion(p):
    ''' instruccion : pmain
                    | petiqueta'''
    p[0] = p[1]
    
def p_pmain(p):
    'pmain : MAIN DOSPUNTOS sentencias '
    nodo2 = NodoG(getIndex(),"pmain",[])
    nodo2.add(NodoG(getIndex(),"main", None))
    nodo2.add(NodoG(getIndex(),":", None))
    for item in p[3].nodo:
        nodo2.add(item)
    p[0] = Nodo(Main(p[3].instruccion,p.lineno(1),find_column(p.slice[1])),nodo2) 
    print("pmain : MAIN DOSPUNTOS sentencias; acciones ")
    print("instruccion : pmain; instruccion = pmain")
    

def p_sentencias(p):
    'sentencias    :   sentencias sentencia'
    p[1].instruccion.append(p[2].instruccion)
    p[1].nodo.append(p[2].nodo)
    nodo = NodoG(getIndex(),"sentencias",p[1].nodo)
    p[0] = Nodo(p[1].instruccion,[nodo])
    print("sentencias : sentencias sentencia; sentencias2.append(sentencia); sentencias = sentencias2")

def p_sentencias2(p):
    'sentencias    :   sentencia'
    arreglo = []
    arreglo.append(p[1].instruccion)
    p[0]= Nodo(arreglo,[NodoG(getIndex(),"sentencia",[p[1].nodo])])
    print("sentencias : sentencia; sentencias2 = new lista; sentencias2.append(sentencia)")

def p_sentencia(p):
    '''sentencia : pvariable
    '''
    p[0] = p[1]

def p_pvariable(p):
    'pvariable : VARIABLE IGUAL operacion PYCOMA'
    nodo = NodoG(getIndex(),"pvariable",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(p[3].nodo)
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = Nodo(Asignacion(p[1],p[3].instruccion,Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1])),nodo)
    
    print('sentencia: pvariable; { sentencia = pvariable}')

def p_operaciones(p):
    ''' operacion   :   valor MAS valor
                    |   valor MENOS valor
                    |   valor MULTIPLICACION valor
                    |   valor DIVISION valor
                    |   valor MODULAR valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(p[1].nodo)
    nodo.add(NodoG(getIndex(),p[2], None))
    nodo.add(p[3].nodo)

    if p[2] == '+': p[0] = Nodo(OperacionBinaria(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.SUMA,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '-': p[0] = Nodo(OperacionBinaria(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.RESTA,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '*': p[0] = Nodo(OperacionBinaria(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.MULTIPLICACION,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '/': p[0] = Nodo(OperacionBinaria(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.DIVISION,p.lineno(2),find_column(p.slice[2])),nodo)
    elif p[2] == '%': p[0] = Nodo(OperacionBinaria(p[1].instruccion,p[3].instruccion,OPERACION_NUMERICA.MODULAR,p.lineno(2),find_column(p.slice[2])),nodo)

def p_operacion(p):
    ' operacion     :   valor '
    nodo = NodoG(getIndex(),"operacion",[p[1].nodo])
    
    p[0]=Nodo(p[1].instruccion,nodo)

def p_valor(p):
    '''valor    :   ENTERO
                |   DECIMAL
    '''
    p[0] = Nodo(OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1])),NodoG(getIndex(),str(p[1]), None))

def p_valor2(p):
    '''valor    :   CADENA
                |   CARACTER
    '''
    p[0] = Nodo(OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1])),p[1])

def p_valor3(p):
    '''valor    :   VARIABLE
    '''
    p[0] = Nodo(OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1])),p[1])

def p_petiqueta(p):
    'petiqueta : ID DOSPUNTOS sentencias'
    nodo2 = NodoG(getIndex(),"petiqueta",[])
    nodo2.add(NodoG(getIndex(),p[1], None))
    nodo2.add(NodoG(getIndex(),":", None))
    for item in p[3].nodo:
        nodo2.add(item)
    p[0] = Nodo(Etiqueta(p[1],p[3].instruccion,p.lineno(1),find_column(p.slice[1])),nodo2)
    print("petiqueta : "+p[1]+" DOSPUNTOS sentencias; acciones ")
    print("instruccion : petiqueta; instruccion = petiqueta")

def p_error(p):
     if not p:
         print("End of File!")
         return
 
     # Read ahead looking for a closing '}'
     while True:
         tok = parser.token()             # Get the next token
         if not tok or tok.type == 'PYCOMA': 
             break
     parser.restart()

parser = yacc.yacc()

input = ""
def parse(inpu) :
    global input
    input = inpu
    return parser.parse(inpu)

def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1