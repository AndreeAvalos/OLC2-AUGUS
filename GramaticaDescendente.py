import ply.yacc as yacc
import ply.lex as lex

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
    print("Illegal character '%s'" % t.value[0])
    #agregarError('Lexico',"Caracter \'{0}\' ilegal".format(t.value[0]), t.lexer.lineno+1,find_column(t))
    t.lexer.skip(1)

lexer = lex.lex()
def p_init(p):
    'init : instrucciones'
    p[0] = None

def p_instrucciones(p):
    'instrucciones  :   instruccion instruccionesP'

def p_instruccionesP(p):
    '''instruccionesP   :   instruccion instruccionesP
                        |   empty
    '''

def p_instruccion(p):
    '''instruccion  :   main
                    |   etiqueta
                    
    '''
def p_main(p):
    'main   :   MAIN DOSPUNTOS main2'

def p_main2(p):
    '''main2    :   sentencias
                |   empty
    '''

def p_etiqueta(p):
    'etiqueta   :   ID DOSPUNTOS etiqueta2'

def p_etiqueta2(p):
    '''etiqueta2    :   sentencias
                    |   empty
    '''

def p_sentencias(P):
    'sentencias :   sentencia sentenciasP'

def p_sentenciasP(p):
    '''sentenciasP      :   sentencia sentenciasP
                        |   empty
    '''
def p_sentencia(p):
    '''sentencia    :   aux1
                    |   pgoto
                    |   pexit
                    |   punset
                    |   pif
                    |   pprint
                    |   pread
    '''

def p_aux1(p):
    'aux1   :   VARIABLE aux2'

def p_aux2(p):
    '''aux2 :   IGUAL aux3
            |   dimensiones IGUAL operacion PYCOMA
    '''
def p_aux3(p):
    '''aux3 :   ARRAY PARIZQ PARDER PYCOMA
            |   operacion PYCOMA
            |   READ PARIZQ PARDER PYCOMA
            |   ANDBIT VARIABLE PYCOMA
    '''
def p_dimensiones(p):
    'dimensiones    :   dimension dimensionesP'

def p_dimensionesP(p):
    '''dimensionesP     :   dimension dimensionesP
                        |   empty
    '''
def p_dimension(p):
    'dimension  :   CORIZQ valor CORDER'

def p_goto(p):
    'pgoto  :   GOTO ID PYCOMA'

def p_exit(p):
    'pexit  :   EXIT PYCOMA'

def p_unset(p):
    'punset :   UNSET PARIZQ VARIABLE PARDER PYCOMA'

def p_if(p):
    'pif    :   IF PARIZQ operacion PARDER GOTO ID PYCOMA'

def p_print(p):
    'pprint :   PRINT PARIZQ aux4 PARDER PYCOMA'

def p_read(p):
    'pread  :   READ PARIZQ PARDER PYCOMA'

def p_aux4(p):
    '''aux4 :   VARIABLE aux5
            |   CADENA2
    '''
def p_aux5(p):
    '''aux5 :   dimensiones
            |   empty
    '''
def p_operacion(p):
    '''operacion    :   valor operacionP
                    |   NOT valor
                    |   NOTBIT valor
                    |   MENOS valor
                    |   ABS PARIZQ aux6 PARDER
                    |   PARIZQ aux7
    '''
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
                    |   empty
    '''
def p_aux6(p):
    '''aux6 :   valor
            |   MENOS valor
    '''

def p_aux7(p):
    '''aux7 :   INTEGER PARDER VARIABLE
            |   FLOAT  PARDER VARIABLE
            |   CHAR  PARDER  VARIABLE
    '''
def p_aux8(p):
    '''aux8 :   dimensiones
            |   empty
    '''
def p_valor(p):
    '''valor    :   ENTERO
                |   DECIMAL
                |   CADENA
                |   CADENA2
                |   VARIABLE aux8
    '''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    global parser
    print(p)
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
    return parser.parse(inpu)