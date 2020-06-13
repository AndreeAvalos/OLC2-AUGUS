import ply.yacc as yacc
import ply.lex as lex
from Instruccion import *
from Operacion import *
import subprocess
from Recolectar import TokenError
from Gramatica import NodoGramatical

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
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    #editar para agregar a una tabla
    #print("Illegal character '%s'" % t.value[0])
    agregarError('Lexico',"Caracter \'{0}\' ilegal".format(t.value[0]), t.lexer.lineno+1,find_column(t))
    t.lexer.skip(1)

stack = []
lstGrmaticales = []
def p_init(p):
    'init : instrucciones'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("initi-> instrucciones")
    gramatical.add("init.val=instrucciones.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = p[1]

def p_instrucciones(p):
    'instrucciones  :   instruccion instruccionesP'
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("instrucciones->instruccion sentenciasP")
    gramatical.add("instruccionesP.val.append(instruccion)")
    gramatical.add("instrucciones.val = instruccionesP.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[2].insert(0,p[1])
    p[0] = p[2]

def p_instruccionesP(p):
    '''instruccionesP   :   instruccion instruccionesP
    '''
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("instruccionesP->instruccion sentenciasP")
    gramatical.add("instruccionesP2.val.append(instruccion)")
    gramatical.add("instruccionesP.val = instruccionesP2.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[2].insert(0,p[1])
    p[0] = p[2]
def p_instruccionesP2(p):
    'instruccionesP   :'
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("instruccionesP->empty")
    gramatical.add("instruccionesP.val = new list[]")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = []


def p_instruccion(p):
    '''instruccion  :   main
                    |   etiqueta          
    ''' 
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("instruccion-> {0}".format(p.slice[1].type))
    gramatical.add("instrucion.val = {0}.val".format(p.slice[1].type))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = p[1]

def p_main(p):
    'main   :   MAIN DOSPUNTOS sentencias'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pmain-> MAIN DOSPUNTOS sentencias")
    gramatical.add("pmain.val = Main(sentencias.val)")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Main(p[3],p.lineno(1),find_column(p.slice[1]))


def p_main2(p):
    '''main    :   MAIN DOSPUNTOS
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pmain-> MAIN DOSPUNTOS epsilon")
    gramatical.add("pmain.val = Main(epsilon)")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Main(Vacio(),p.lineno(1),find_column(p.slice[1]))

def p_etiqueta(p):
    'etiqueta   :   ID DOSPUNTOS sentencias'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("petiqueta-> ID DOSPUNTOS sentencias")
    gramatical.add("petiqueta.val = Etiqueta({0},sentencias.val)".format(p[1]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Etiqueta(p[1],p[3],p.lineno(1),find_column(p.slice[1]))

def p_etiqueta2(p):
    'etiqueta : ID DOSPUNTOS '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("petiqueta-> ID DOSPUNTOS epsilon")
    gramatical.add("petiqueta.val = Etiqueta({0},epsilon)".format(p[1]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Etiqueta(p[1],Vacio(),p.lineno(1),find_column(p.slice[1]))

def p_sentencias(p):
    'sentencias :   sentencia sentenciasP'
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("sentencias->sentencia sentenciasP")
    gramatical.add("sentencias.val.append(sentencia)")
    gramatical.add("sentenciasP.val = sentenciasP.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[2].insert(0,p[1])
    p[0] = p[2]


def p_sentenciasP2(p):
    '''sentenciasP      :   sentencia sentenciasP
    '''
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("sentenciasP->sentencia sentenciasP")
    gramatical.add("sentenciasP2.val.append(sentencia)")
    gramatical.add("sentenciasP.val = sentenciasP2.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[2].insert(0,p[1])
    p[0] = p[2]

def p_sentenciasP(p):
    '''sentenciasP      :
    '''
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("sentenciasP->empty")
    gramatical.add("sentenciasP.val = new list[]")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
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
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("sentencia-> {0}".format(p.slice[1].type))
    gramatical.add("sentencia.val = {0}.val".format(p.slice[1].type))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = p[1]

def p_array(p):
    'parray :   VARIABLE IGUAL ARRAY PARIZQ PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("parray-> VARIABLE IGUAL ARRAY PARIZQ PARDER PYCOMA")
    gramatical.add("parray.val = DeclararArreglo({0})".format(p[1]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = DeclararArreglo(p[1],p.lineno(1),find_column(p.slice[1]))

def p_pvariable(p):
    'pvariable : VARIABLE IGUAL operacion PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pvariable-> VARIABLE IGUAL operacion PYCOMA")
    gramatical.add("pvariable.val = Asignacion({0},operacion.val)".format(p[1]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Asignacion(p[1],p[3],Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1]))

def p_arreglo(p):
    'parreglo   :   VARIABLE dimensiones IGUAL operacion PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("parreglo-> VARIABLE dimensiones IGUAL operacion PYCOMA")
    gramatical.add("pvariable.val = Asignacion({0},operacion.val)".format(p[1]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = AsignacionArreglo(p[1],p[2],p[4],p.lineno(1),find_column(p.slice[1]))

def p_dimensiones(p):
    'dimensiones    :   dimension dimensionesP'
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("dimensiones->dimension dimensionesP")
    gramatical.add("dimensionesP.val.append(dimension)")
    gramatical.add("dimensiones.val = dimensionesP2.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[2].insert(0,p[1])
    p[0] = p[2]

def p_dimensionesP(p):
    'dimensionesP     :   dimension dimensionesP '
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("dimensionesP->dimension dimensionesP")
    gramatical.add("dimensionesP2.val.append(dimension)")
    gramatical.add("dimensionesP.val = dimensionesP2.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[2].insert(0,p[1])
    p[0] = p[2]

def p_dimensionesP2(p):
    'dimensionesP     :   '
    #Parte para reporte Gramatical 
    gramatical = NodoGramatical("dimensionesP->empty")
    gramatical.add("dimensionesP.val = new list[]")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = []

def p_dimension(p):
    'dimension  :   CORIZQ valor CORDER'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("dimension-> CORIZQ valor CORDER")
    gramatical.add("dimension.val = valor.val")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = p[2]

def p_prefencia(p):
    'preferencia    :  VARIABLE IGUAL ANDBIT VARIABLE PYCOMA '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("preferencia-> VARIABLE IGUAL ANDBIT VARIABLE PYCOMA ")
    gramatical.add("preferencia.val = Referencia({0},OperacionVariable({1}))".format(p[1],p[4]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Referencia(p[1],OperacionVariable(p[4],p.lineno(4),find_column(p.slice[4])),Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1]))

def p_pgoto(p):
    'pgoto  :   GOTO ID PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pgoto-> GOTO ID PYCOMA")
    gramatical.add("pgoto.val = Goto({0})".format(p[2]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Goto(p[2],p.lineno(1),find_column(p.slice[1]))

def p_psalir(p):
    'pexit  :   EXIT PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pexit-> EXIT PYCOMA")
    gramatical.add("pexit.val = Exit()")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Exit(p.lineno(1),find_column(p.slice[1]))

def p_punset(p):
    'punset  :   UNSET PARIZQ VARIABLE PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("punset-> UNSET PARIZQ VARIABLE PARDER PYCOMA")
    gramatical.add("punset.val = unset({0})".format(p[3]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = UnSet(p[3],p.lineno(1),find_column(p.slice[1]))

def p_pif(p):
    'pif    :   IF PARIZQ operacion PARDER GOTO ID PYCOMA '
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pif-> IF PARIZQ operacion PARDER GOTO ID PYCOMA")
    gramatical.add("pif.val = If_(operacion.val,goto({0}))".format(p[6]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = If_(p[3],Goto(p[6],p.lineno(1),find_column(p.slice[1])),p.lineno(1),find_column(p.slice[1]))

def p_pprint(p):
    '''pprint   :   PRINT PARIZQ valor PARDER PYCOMA
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pprint-> PRINT PARIZQ VARIABLE dimensiones PARDER PYCOMA")
    gramatical.add("pprint.val = Print_(OperacionArreglo({0},dimensiones.val))".format(p.slice[3].type))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Print_(p[3], p.lineno(1),find_column(p.slice[1]))

def p_pprint3(p):
    'pprint :  PRINT PARIZQ VARIABLE dimensiones PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pprint-> PRINT PARIZQ valor PARDER PYCOMA")
    gramatical.add("pprint.val = Print_(Nueva linea)")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Print_(OperacionArreglo(p[3],p[4],p.lineno(3),find_column(p.slice[3])),p.lineno(3),find_column(p.slice[3]))
def p_pread(p):
    'pread  :   VARIABLE IGUAL READ PARIZQ PARDER PYCOMA'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("pread-> VARIABLE IGUAL READ PARIZQ PARDER PYCOMA")
    gramatical.add("pread.val = Read(Asignacion({0}))".format(p[1]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = Read(Asignacion(p[1],None,Tipo_Etiqueta.VARIABLE,p.lineno(1),find_column(p.slice[1])),p.lineno(1),find_column(p.slice[1]))

def p_operacion(p):
    '''operacion    :   NOT valor
                    |   NOTBIT valor
                    |   MENOS valor
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> {0} valor".format(p.slice[1].type))
    #Parte para AST
    if p[1] == '!':
        #Parte para reporte Gramatical
        gramatical.add("operacion.val = OperacionUnaria(valor.val,NOT)")
        #Parte para AST
        p[0] = OperacionUnaria(p[2],OPERACION_LOGICA.NOT,p.lineno(1),find_column(p.slice[1]))
    elif p[1] == '~':
        #Parte para reporte Gramatical
        gramatical.add("operacion.val = OperacionUnaria(valor.val,NOTBIT)")
        #Parte para AST
        p[0] = OperacionUnaria(p[2],OPERACION_BIT.NOT,p.lineno(1),find_column(p.slice[1]))
    elif p[1] == '-':
        #Parte para reporte Gramatical
        gramatical.add("operacion.val = OperacionUnaria(valor.val,RESTA)")
        #Parte para AST
        p[0] = OperacionUnaria(p[2],OPERACION_NUMERICA.RESTA,p.lineno(1),find_column(p.slice[1]))
    #Parte para reporte Gramatical
    lstGrmaticales.insert(0,gramatical)
        

def p_operaciones5(p):
    'operacion  :   ABS PARIZQ valor PARDER'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> ABS PARIZQ valor PARDER")
    gramatical.add("operacion.val = OperacionUnaria(valor.val,ABSOLUTO)")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = OperacionUnaria(p[3],OPERACION_NUMERICA.ABSOLUTO,p.lineno(1),find_column(p.slice[1]))

def p_operaciones6(p):
    'operacion  :   ABS PARIZQ MENOS valor PARDER'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> ABS PARIZQ MENOS valor PARDER")
    gramatical.add("operacion.val = OperacionUnaria(valor.val,ABSOLUTO)")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = OperacionUnaria(p[4],OPERACION_NUMERICA.ABSOLUTO,p.lineno(1),find_column(p.slice[1]))


def p_operacion7(p):
    'operacion  :   VARIABLE dimensiones'
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> VARIABLE dimensiones")
    gramatical.add("operacion.val = OperacionArreglo(dimensiones.val,dimensiones.val)")
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = OperacionArreglo(p[1],p[2],p.lineno(1),find_column(p.slice[1]))

def p_operacion8(p):
    '''operacion    :   PARIZQ INTEGER PARDER valor
                    |   PARIZQ FLOAT PARDER valor
                    |   PARIZQ CHAR PARDER valor
    '''
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacion-> PARIZQ {0} PARDER valor".format(p.slice[2].type))
    gramatical.add("operacion.val = OperacionCasteo({0},valor.val)".format(p[2]))
    lstGrmaticales.insert(0,gramatical)
    #Parte para AST
    p[0] = OperacionCasteo(p[2],p[4],p.lineno(1),find_column(p.slice[1]))

def p_operacion2(p):
    '''operacion    :   valor operacionP
    '''
    #Parte para Reglas Gramaticales
    gramatical = NodoGramatical("operacion    ->   valor operacionP")
    gramatical.add("operacion.valor = operacionP.valor")
    lstGrmaticales.insert(0,gramatical)
    #Parte para instrucciones 
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
    #Parte para reporte Gramatical
    gramatical = NodoGramatical("operacionP -> {0} valor".format(p.slice[1].type))
    gramatical.add("op2 = stack.pop()")
    gramatical.add("op1 = stack.pop()")
    #Parte para instrucciones 
    op2 = stack.pop()#obtenemos el segundo operador en la pila
    op1 = stack.pop()#optenemos el primer operador en la pila
    if p.slice[1].type == 'MAS':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionNumerica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.SUMA,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MENOS':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionNumerica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.RESTA,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MULTIPLICACION':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionNumerica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.MULTIPLICACION,p.lineno(1),find_column(p.slice[1])) 
    elif p.slice[1].type == 'DIVISION':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionNumerica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.DIVISION,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MODULAR':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionNumerica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionNumerica(op1,op2,OPERACION_NUMERICA.MODULAR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'AND':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionLogica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionLogica(op1,op2,OPERACION_LOGICA.AND,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'OR':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionLogica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionLogica(op1,op2,OPERACION_LOGICA.OR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'XOR':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionLogica(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionLogica(op1,op2,OPERACION_LOGICA.XOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'IGUALIGUAL':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionRelacional(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.IGUAL,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'DIFERENTE':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionRelacional(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.DIFERENTE,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MAYOR':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionRelacional(op1,op2,{0})".format(p.slice[1].type))
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MAYOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MENOR':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionRelacional(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MENOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MAYORIGUAL':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionRelacional(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MAYORQUE,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'MENORIGUAL':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionRelacional(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionRelacional(op1,op2,OPERACION_RELACIONAL.MENORQUE,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'ANDBIT':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionBit(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.AND,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'XORBIT':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionBit(op1,op2,{0})".format(p.slice[1].type))
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.XOR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'ORBIT':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionBit(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.OR,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'SHIFTIZQ':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionBit(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.SHIFTIZQ,p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'SHIFTDER':
         #Parte para reporte Gramatical
        gramatical.add("operacionP = OperacionBit(op1,op2,{0})".format(p.slice[1].type))
        #Parte para instrucciones 
        p[0] = OperacionBit(op1,op2,OPERACION_BIT.SHIFTDER,p.lineno(1),find_column(p.slice[1]))
    #Parte para reporte Gramatical 
    lstGrmaticales.insert(0,gramatical)
    

def p_operacionP2(p):
    'operacionP :   '
    gramatical = NodoGramatical("operacion-> empty")
    gramatical.add("operacionP.val = stack.pop() ")
    lstGrmaticales.insert(0,gramatical)
    p[0] = stack.pop()

def p_valor(p):
    '''valor    :   ENTERO
                |   DECIMAL
                |   CADENA
                |   CADENA2
                |   VARIABLE 
    '''
    #Nodo para Reporte Gramatical 
    gramatical = NodoGramatical("operacion-> {0}".format(p.slice[1].type))
    #retorno de instruccion
    if p.slice[1].type == 'ENTERO' or p.slice[1].type == 'DECIMAL':
        #Nodo para Reporte Gramatical 
        gramatical.add("operacion.val = OperacionNumero({0})".format(p[1]))
        #retorno de instruccion
        p[0] = OperacionNumero(p[1],p.lineno(1),find_column(p.slice[1]))
    elif p.slice[1].type == 'CADENA' or p.slice[1].type == 'CADENA2':
        #Nodo para Reporte Gramatical 
        gramatical.add("operacion.val = OperacionCadena({0})".format(p[1]))
        #retorno de instruccion
        p[0] = OperacionCadena(p[1],p.lineno(1),find_column(p.slice[1]))
    else:
        #Nodo para Reporte Gramatical 
        gramatical.add("operacion.val = OperacionCopiaVariable({0})".format(p[1]))
        #retorno de instruccion
        p[0] = OperacionCopiaVariable(p[1],p.lineno(1),find_column(p.slice[1]))
    #Nodo para Reporte Gramatical
    lstGrmaticales.insert(0,gramatical)
    #Agregamos el valor al stack para poder manejarlo en la siguiente operacion
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
    lexer = lex.lex()
    input = inpu
    return parser.parse(inpu, lexer=lexer)

def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1