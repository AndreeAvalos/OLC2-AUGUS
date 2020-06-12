import ply.yacc as yacc
import ply.lex as lex
from Instruccion import *
from Operacion import *
import subprocess
from Recolectar import TokenError

lst_errores = []

def cmd(commando):
    subprocess.run(commando, shell=True)

def agregarError(tipo,descripcion,line,column):
    global lst_errores
    new_error = TokenError(tipo,descripcion,line,column)
    lst_errores.append(new_error)

def graficarErrores():
    global lst_errores

    try:
        file = open("ELS.dot", "w")
        file.write("digraph tablaErrores{\n")
        file.write("graph [ratio=fill];node [label=\"\\N\", fontsize=15, shape=plaintext];\n")
        file.write("graph [bb=\"0,0,352,154\"];\n")
        file.write("arset [label=<")
        file.write("<TABLE ALIGN=\"LEFT\">\n")
        file.write("<TR><TD>TIPO</TD><TD>DESCRIPCION</TD><TD>LINEA</TD><TD>COLUMNA</TD></TR>\n")
        for token in lst_errores:
            file.write("<TR>")
            file.write("<TD>")
            file.write(token.tipo)
            file.write("</TD>")
            file.write("<TD>")
            file.write(token.descripcion)
            file.write("</TD>")
            file.write("<TD>")
            file.write(str(token.line))
            file.write("</TD>")
            file.write("<TD>")
            file.write(str(token.column))
            file.write("</TD>")
            file.write("</TR>\n")
        file.write("</TABLE>")
        file.write("\n>, ];\n")
        file.write("}")
    except:
        print("ERROR AL ESCRIBIR TABLA")
    finally:
        file.close()
        cmd("dot -Tpng ELS.dot -o ELS.png")

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
    agregarError('Lexico',"Caracter \'{0}\' ilegal".format(t.value[0]), t.lexer.lineno+1,find_column(t))
    t.lexer.skip(1)

stack = []

lexer = lex.lex()
def p_init(p):
    'init : instrucciones'
    p[0] = p[1]

def p_instrucciones(p):
    'instrucciones  :   instruccion instruccionesP'
    p[2].insert(0,p[1])
    p[0] = p[2]
def p_instruccionesP(p):
    '''instruccionesP   :   instruccion instruccionesP
    '''
    p[2].insert(0,p[1])
    p[0] = p[2]
def p_instruccionesP2(p):
    'instruccionesP   :'
    p[0] = []


def p_instruccion(p):
    '''instruccion  :   main
                    |   etiqueta          
    '''   
    p[0] = p[1]

def p_main(p):
    'main   :   MAIN DOSPUNTOS sentencias'
    p[0] = Main(p[3],p.lineno(1),find_column(p.slice[1]))


def p_main2(p):
    '''main    :   MAIN DOSPUNTOS
    '''
    p[0] = Main(Vacio(),p.lineno(1),find_column(p.slice[1]))

def p_etiqueta(p):
    'etiqueta   :   ID DOSPUNTOS sentencias'
    p[0] = Etiqueta(p[1],p[3],p.lineno(1),find_column(p.slice[1]))

def p_etiqueta2(p):
    'etiqueta : ID DOSPUNTOS '
    p[0] = Etiqueta(p[1],Vacio(),p.lineno(1),find_column(p.slice[1]))

def p_sentencias(p):
    'sentencias :   sentencia sentenciasP'
    p[2].insert(0,p[1])
    p[0] = p[2]


def p_sentenciasP2(p):
    '''sentenciasP      :   sentencia sentenciasP
    '''
    p[2].insert(0,p[1])
    p[0] = p[2]

def p_sentenciasP(p):
    '''sentenciasP      :
    '''
    p[0] = []

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
    p[0] = DeclararArreglo(p[1],p.lineno(1),find_column(p.slice[1]))

def p_pvariable(p):
    'pvariable : VARIABLE IGUAL operacion PYCOMA'
    p[0] = Asignacion(p[1],p[3],Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1]))

def p_arreglo(p):
    'parreglo   :   VARIABLE dimensiones IGUAL operacion PYCOMA'
    p[0] = AsignacionArreglo(p[1],p[2],p[4],p.lineno(1),find_column(p.slice[1]))

def p_dimensiones(p):
    'dimensiones    :   dimension dimensionesP'
    p[2].insert(0,p[1])
    p[0] = p[2]

def p_dimensionesP(p):
    'dimensionesP     :   dimension dimensionesP '
    p[2].insert(0,p[1])
    p[0] = p[2]

def p_dimensionesP2(p):
    'dimensionesP     :   '
    p[0] = []

def p_dimension(p):
    'dimension  :   CORIZQ valor CORDER'
    p[0] = p[2]

def p_prefencia(p):
    'preferencia    :  VARIABLE IGUAL ANDBIT VARIABLE PYCOMA '''
    p[0] = Referencia(p[1],OperacionVariable(p[4],p.lineno(4),find_column(p.slice[4])),Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1]))

def p_pgoto(p):
    'pgoto  :   GOTO ID PYCOMA'
    p[0] = Goto(p[2],p.lineno(1),find_column(p.slice[1]))

def p_psalir(p):
    'pexit  :   EXIT PYCOMA'
    p[0] = Exit(p.lineno(1),find_column(p.slice[1]))

def p_punset(p):
    'punset  :   UNSET PARIZQ VARIABLE PARDER PYCOMA'
    p[0] = UnSet(p[3],p.lineno(1),find_column(p.slice[1]))

def p_pif(p):
    'pif    :   IF PARIZQ operacion PARDER GOTO ID PYCOMA '
    p[0] = If_(p[3],Goto(p[6],p.lineno(1),find_column(p.slice[1])),p.lineno(1),find_column(p.slice[1]))

def p_pprint(p):
    '''pprint   :   PRINT PARIZQ VARIABLE PARDER PYCOMA
    '''
    p[0] = Print_(OperacionCopiaVariable(p[3],p.lineno(1),find_column(p.slice[1])),p.lineno(1),find_column(p.slice[1]))

def p_pprint2(p):
    '''pprint   :   PRINT PARIZQ CADENA2 PARDER PYCOMA
    '''
    p[0] = Print_("-",p.lineno(1),find_column(p.slice[1]))

def p_pprint3(p):
    'pprint :  PRINT PARIZQ VARIABLE dimensiones PARDER PYCOMA'
    p[0] = Print_(OperacionArreglo(p[3],p[4],p.lineno(3),find_column(p.slice[3])),p.lineno(3),find_column(p.slice[3]))
def p_pread(p):
    'pread  :   VARIABLE IGUAL READ PARIZQ PARDER PYCOMA'
    p[0] = Read(Asignacion(p[1],None,Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1])),p.lineno(1),find_column(p.slice[1]))

def p_operacion(p):
    '''operacion    :   NOT valor
                    |   NOTBIT valor
                    |   MENOS valor
    '''
    if p[1] == '!':
        p[0] = OperacionUnaria(p[2],OPERACION_LOGICA.NOT,p.lineno(1),find_column(p.slice[1]))
    elif p[1] == '~':
        p[0] = OperacionUnaria(p[2],OPERACION_BIT.NOT,p.lineno(1),find_column(p.slice[1]))
    elif p[1] == '-':
        p[0] = OperacionUnaria(p[2],OPERACION_NUMERICA.RESTA,p.lineno(1),find_column(p.slice[1]))
        

def p_operaciones5(p):
    'operacion  :   ABS PARIZQ valor PARDER'
    p[0] = OperacionUnaria(p[3],OPERACION_NUMERICA.ABSOLUTO,p.lineno(1),find_column(p.slice[1]))

def p_operaciones6(p):
    'operacion  :   ABS PARIZQ MENOS valor PARDER'
    p[0] = OperacionUnaria(p[4],OPERACION_NUMERICA.ABSOLUTO,p.lineno(1),find_column(p.slice[1]))


def p_operacion7(p):
    'operacion  :   VARIABLE dimensiones'
    p[0] = OperacionArreglo(p[1],p[2],p.lineno(1),find_column(p.slice[1]))

def p_operacion8(p):
    '''operacion    :   PARIZQ INTEGER PARDER valor
                    |   PARIZQ FLOAT PARDER valor
                    |   PARIZQ CHAR PARDER valor
    '''
    p[0] = OperacionCasteo(p[2],p[4].instruccion,p.lineno(1),find_column(p.slice[1]))

def p_operacion2(p):
    '''operacion    :   valor operacionP
    '''
    p[0] = p[2]


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
    op2 = stack.pop()
    op1 = stack.pop()
    if p.slice[1].type == 'MAS':
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.SUMA,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MENOS':
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.RESTA,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MULTIPLICACION':
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.MULTIPLICACION,p.lineno(1),find_column(p.slice[1])) 
    elif p.slice[1].type == 'DIVISION':
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.DIVISION,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MODULAR':
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.MODULAR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'AND':
        p[0] = OperacionLogica(op1,op2,OPERACION_LOGICA.AND,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'OR':
        p[0] = OperacionLogica(op1,op2,OPERACION_LOGICA.OR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'XOR':
        p[0] = OperacionLogica(op1,op2,OPERACION_LOGICA.XOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'IGUALIGUAL':
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.IGUAL,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'DIFERENTE':
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.DIFERENTE,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MAYOR':
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MAYOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MENOR':
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MENOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MAYORIGUAL':
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MAYORQUE,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MENORIGUAL':
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MENORQUE,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'ANDBIT':
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.AND,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'XORBIT':
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.XOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'ORBIT':
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.OR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'SHIFTIZQ':
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.SHIFTIZQ,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'SHIFTDER':
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.SHIFTDER,p.lineno(1),find_column(p.slice[1]))
    

def p_operacionP2(p):
    'operacionP :   '

    p[0] = stack.pop()

def p_valor(p):
    '''valor    :   ENTERO
                |   DECIMAL
                |   CADENA
                |   CADENA2
                |   VARIABLE 
    '''

    p[0] = p[1]

    if p.slice[1].type == 'ENTERO' or p.slice[1].type == 'DECIMAL':
        p[0] = OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'CADENA' or p.slice[1].type == 'CADENA2':
        p[0] = OperacionCadena(p[1],p.lineno(1),find_column(p.slice[1]))
    else:
        p[0] = OperacionCopiaVariable(p[1],p.lineno(1),find_column(p.slice[1]))
    stack.append(p[0])



def p_error(p):
    global parser
    agregarError("Sintactico","Sintaxis no reconocida \"{0}\"".format(p.value),p.lineno+1, find_column(p))

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

def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1