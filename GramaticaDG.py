import ply.yacc as yacc
import ply.lex as lex
from Instruccion import *
from Operacion import *
import subprocess
from Recolectar import TokenError
from Gramatica import NodoG




def cmd(commando):
    subprocess.run(commando, shell=True)


def construirAST(nodo):
    try:
        file = open("ASPDescendente.dot", "w")
        file.write("digraph{ \n")
        imprimirNodos(nodo,file)
        graficar(nodo,file)
        file.write("\n}")
    except:
        print("ERROR")
    finally:
        file.close()
        cmd("dot -Tpng ASPDescendente.dot -o ASPDescendente.png")

def imprimirNodos(nodo,file):
    if nodo!= None:
        file.write(str(nodo.index)+"[style = \"filled\" ; label = \""+nodo.nombre+"\"] \n")
        if nodo.childs != None:
            for child in nodo.childs:
                imprimirNodos(child, file)

def graficar(nodo,file):
    if nodo != None:
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
    'CADENA',
    'CADENA2',
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
#t_ESCAPE =r'\"\\n\"'

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
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CADENA2(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_COMENTARIO(t):
    r'\#.*'
    t.lexer.lineno += 1



def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    #editar para agregar a una tabla
    #print("Illegal character '%s'" % t.value[0])
    #agregarError('Lexico',"Caracter \'{0}\' ilegal".format(t.value[0]), t.lexer.lineno+1,find_column(t))
    t.lexer.skip(1)

stack = []

lexer = lex.lex()
index = 0
#Metodo para generar un nuevo index
def getIndex():
    global index
    index = index+1
    return index

def p_init(p):
    'init : instrucciones'
    p[0] =  NodoG(getIndex(),"init",[p[1]])

def p_instrucciones(p):
    'instrucciones  :   instruccion instruccionesP'
    nodo = NodoG(getIndex(), "instruciones",[])
    nodo2 = NodoG(getIndex(),"instruccion", [])
    nodo2.add(p[1])
    nodo.add(nodo2)
    nodo.add(p[2])
    p[0] = nodo 

def p_instruccionesP(p):
    '''instruccionesP   :   instruccion instruccionesP
    '''
    nodo = NodoG(getIndex(), "instrucionesP",[])
    nodo2 = NodoG(getIndex(),"instruccion", [])
    nodo2.add(p[1])
    nodo.add(nodo2)
    nodo.add(p[2])
    p[0] = nodo 

def p_instruccionesP2(p):
    'instruccionesP   :'
    p[0] = NodoG(getIndex(), "epsilon", None)



def p_instruccion(p):
    '''instruccion  :   main
                    |   etiqueta          
    '''   
    p[0] = p[1]

def p_main(p):
    'main   :   MAIN DOSPUNTOS sentencias'
    nodo = NodoG(getIndex(), "main",[])
    nodo.add(NodoG(getIndex(),"main",None))
    nodo.add(NodoG(getIndex(),":",None))
    
    nodo.add(p[3])
    p[0] = nodo


def p_main2(p):
    '''main    :   MAIN DOSPUNTOS
    '''
    nodo = NodoG(getIndex(), "main",[])
    nodo.add(NodoG(getIndex(),"main",None))
    nodo.add(NodoG(getIndex(),":",None))
    nodo.add(NodoG(getIndex(),"epsilon",None))
    p[0] = nodo

def p_etiqueta(p):
    'etiqueta   :   ID DOSPUNTOS sentencias'
    nodo = NodoG(getIndex(), "etiqueta",[])
    nodo.add(NodoG(getIndex(),p[1],None))
    nodo.add(NodoG(getIndex(),":",None))
    nodo.add(p[3])
    p[0] = nodo

def p_etiqueta2(p):
    'etiqueta : ID DOSPUNTOS '
    nodo = NodoG(getIndex(), "etiqueta",[])
    nodo.add(NodoG(getIndex(),p[1],None))
    nodo.add(NodoG(getIndex(),":",None))
    nodo.add(NodoG(getIndex(),"epsilon",None))
    p[0] = nodo

def p_sentencias(p):
    'sentencias :   sentencia sentenciasP'
    nodo = NodoG(getIndex(), "sentencias",[])
    nodo2 = NodoG(getIndex(),"sentencia", [])
    nodo2.add(p[1])
    nodo.add(nodo2)
    nodo.add(p[2])
    p[0] = nodo 


def p_sentenciasP2(p):
    '''sentenciasP      :   sentencia sentenciasP
    '''
    nodo = NodoG(getIndex(), "sentenciasP",[])
    nodo2 = NodoG(getIndex(),"sentencia", [])
    nodo2.add(p[1])
    nodo.add(nodo2)
    nodo.add(p[2])
    p[0] = nodo 

def p_sentenciasP(p):
    '''sentenciasP      :
    '''
    p[0] = NodoG(getIndex(), "epsilon", None)


def p_sentencia(p):
    '''sentencia    : pvariable
                    | preferencia
                    | pgoto
                    | pexit
                    | punset
                    | pif
                    | pprint
                    | pread
                    | parreglo
                    | parray
    '''
    p[0] = p[1]

def p_array(p):
    'parray :   VARIABLE IGUAL ARRAY PARIZQ PARDER PYCOMA'
    nodo = NodoG(getIndex(),"parray",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(NodoG(getIndex(),"array()", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_pvariable(p):
    'pvariable : VARIABLE IGUAL operacion PYCOMA'
    nodo = NodoG(getIndex(),"pvariable",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(p[3])
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_arreglo(p):
    'parreglo   :   VARIABLE dimensiones IGUAL operacion PYCOMA'
    nodo = NodoG(getIndex(),"pvariable",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(p[2])
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(p[4])
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_dimensiones(p):
    'dimensiones    :   dimension dimensionesP'
    nodo = NodoG(getIndex(), "dimensiones",[])
    nodo2 = NodoG(getIndex(),"dimension", [])
    nodo2.add(p[1])
    nodo.add(nodo2)
    nodo.add(p[2])
    p[0] = nodo 
def p_dimensionesP(p):
    'dimensionesP     :   dimension dimensionesP '
    nodo = NodoG(getIndex(), "dimensionesP",[])
    nodo2 = NodoG(getIndex(),"dimension", [])
    nodo2.add(p[1])
    nodo.add(nodo2)
    nodo.add(p[2])
    p[0] = nodo 

def p_dimensionesP2(p):
    'dimensionesP     :   '
    p[0] = NodoG(getIndex(), "epsilon", None)

def p_dimension(p):
    'dimension  :   CORIZQ valor CORDER'
    p[0] = p[2]

def p_prefencia(p):
    'preferencia    :  VARIABLE IGUAL ANDBIT VARIABLE PYCOMA '
    nodo = NodoG(getIndex(),"preferencia",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(NodoG(getIndex(),"&", None))
    nodo.add(NodoG(getIndex(),p[4], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_pgoto(p):
    'pgoto  :   GOTO ID PYCOMA'
    nodo = NodoG(getIndex(),"pgoto",[])
    nodo.add(NodoG(getIndex(),"goto", None))
    nodo.add(NodoG(getIndex(),p[2], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_psalir(p):
    'pexit  :   EXIT PYCOMA'
    nodo = NodoG(getIndex(),"pexit",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo 

def p_punset(p):
    'punset  :   UNSET PARIZQ VARIABLE PARDER PYCOMA'
    nodo = NodoG(getIndex(),"punset",[])
    nodo.add(NodoG(getIndex(),"unset", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(NodoG(getIndex(),p[3], None))
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_pif(p):
    'pif    :   IF PARIZQ operacion PARDER GOTO ID PYCOMA '
    nodo = NodoG(getIndex(),"pif",[])
    nodo.add(NodoG(getIndex(),"if", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(p[3])
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),"got", None))
    nodo.add(NodoG(getIndex(),p[6], None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo


def p_pprint(p):
    '''pprint   :   PRINT PARIZQ valor PARDER PYCOMA
    '''
    nodo = NodoG(getIndex(),"pprint",[])
    nodo.add(NodoG(getIndex(),"print", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(p[3])
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_pprint3(p):
    'pprint :  PRINT PARIZQ VARIABLE dimensiones PARDER PYCOMA'
    nodo = NodoG(getIndex(),"pprint",[])
    nodo.add(NodoG(getIndex(),"print", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo2 = NodoG(getIndex(),"operacion",[])
    nodo2.add(NodoG(getIndex(),p[3], None))
    nodo2.add(p[4])
    nodo.add(nodo2)
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_pread(p):
    'pread  :   VARIABLE IGUAL READ PARIZQ PARDER PYCOMA'
    nodo = NodoG(getIndex(),"pread",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(NodoG(getIndex(),"=", None))
    nodo.add(NodoG(getIndex(),"read", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_operacion(p):
    '''operacion    :   NOT valor
                    |   NOTBIT valor
                    |   MENOS valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(p[2])
    p[0] = nodo
        

def p_operaciones5(p):
    'operacion  :   ABS PARIZQ valor PARDER'
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),"abs", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(p[3])
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo

def p_operaciones6(p):
    'operacion  :   ABS PARIZQ MENOS valor PARDER'
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),"abs", None))
    nodo.add(NodoG(getIndex(),"(", None))
    nodo.add(NodoG(getIndex(),"-", None))
    nodo.add(p[4])
    nodo.add(NodoG(getIndex(),")", None))
    nodo.add(NodoG(getIndex(),";", None))
    p[0] = nodo


def p_operacion7(p):
    'operacion  :   VARIABLE dimensiones'
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),p[1], None))
    nodo.add(p[2])
    p[0] = nodo

def p_operacion8(p):
    '''operacion    :   PARIZQ INTEGER PARDER valor
                    |   PARIZQ FLOAT PARDER valor
                    |   PARIZQ CHAR PARDER valor
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(NodoG(getIndex(),"(",None))
    nodo.add(NodoG(getIndex(),p[2],None))
    nodo.add(NodoG(getIndex(),")",None))
    nodo.add(p[4])
    p[0] = nodo

def p_operacion2(p):
    '''operacion    :   valor operacionP
    '''
    nodo = NodoG(getIndex(),"operacion",[])
    nodo.add(p[1])
    nodo.add(p[2])

    p[0] = nodo


def p_operacionP(p):
    '''operacionP   :   MAS valor
                    |   MENOS valor
                    |   MULTIPLICACION valor
                    |   DIVISION valor
                    |   MODULAR valor
                    |   AND valor
                    |   OR valor
                    |   XOR valor
                    |   IGUALIGUAL valor
                    |   DIFERENTE valor
                    |   MAYOR valor
                    |   MENOR valor
                    |   MAYORIGUAL valor
                    |   MENORIGUAL valor
                    |   ANDBIT valor
                    |   ORBIT valor
                    |   XORBIT  valor
                    |   SHIFTIZQ valor
                    |   SHIFTDER valor
    '''

    nodo = NodoG(getIndex(),"operacionP",[])
    nodo.add(NodoG(getIndex(), p[1],None))
    nodo.add(p[2])
    p[0] = nodo
    

def p_operacionP2(p):
    'operacionP :   '
    
    p[0] = NodoG(getIndex(),"epsilon",None)

def p_valor(p):
    '''valor    :   ENTERO
                |   DECIMAL
                |   CADENA
                |   CADENA2
                |   VARIABLE 
    '''

    p[0] = NodoG(getIndex(), str(p[1]),None)



def p_error(p):
    global parser
    #agregarError("Sintactico","Sintaxis no reconocida \"{0}\"".format(p.value),p.lineno+1, find_column(p))

    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'PYCOMA': 
            break
    parser.errok()

    return tok

parser = yacc.yacc()

input = ""
def parse(inpu) :
    global input
    global lexer
    lexer.lineno=0
    input = inpu
    global index
    index = 0
    return parser.parse(inpu)

def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1