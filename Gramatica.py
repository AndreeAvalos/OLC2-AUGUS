import ply.yacc as yacc
import ply.lex as lex
parser = yacc.yacc()
lexer = lex.lex()


reservadas = {
    #Tipos para castear
    'int': 'ENTERO',
    'float': 'FLOAT',
    'char': 'CHAR',
    'print': 'PRINT',
    '$ra': 'SIMULADOR',
    '$sp': 'PUNTERO',
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
    'CHAR',
    'CADENA',
    'ID',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULAR',
    'NOT',
    'AND',
    'OR',
    'NOTBIT',
    'ANDBIT',
    'ORBIT',
    'XORBIT',
    'SHIFTIZQ',
    'SHIFTDER'
] + list(reservadas.values())

t_PYCOMA = r';'
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
t_POR = r'\*'
t_DIVIDIDO = r'/'
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
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CHAR(t):
    r'\'[a-zA-Z]\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_COMENTARIO(t):
    r'#.*\n'
    t.lexer.lineno += 1


def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    #editar para agregar a una tabla
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


precedence = (
    ('left','XOR'),
    ('left','AND'),
    ('left','NOT'),
    ('left','IGUALIGUAL', 'DIFERENTE','MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO', 'MODULAR'),
    ('right','UMENOS'),
    )

