import ply.lex as lex

# resultado del analisis
resultado_lexema = []

reservada = (
    # Palabras Reservadas
    'cos',
    'sin',
    'tan',
)
tokens = reservada + (
    'IDENTIFICADOR',
    'ENTERO',
  

    #Operaciones regulares
    'SUMA', # +
    'RESTA',# -
    'MULT', # *
    'DIV', # /
    'POTENCIA', # ** o ^
    'MODULO', # %

    #Operaciones especiales
   #'TRIG', #sin, cos, tan

    
    # Symbolos
    'IGUAL', #=
    'PARIZQ',#(
    'PARDER',#)
    'MINUSMINUS',
    'PLUSPLUS',
    'ASIGNAR'
    
    # Otros
   # 'PUNTOCOMA', #;
)

# Reglas de Expresiones Regulares para token de Contexto simple

t_SUMA = r'\+'
t_RESTA = r'-'
# t_MINUSMINUS = r'\-\-'
# t_PUNTO = r'\.'
t_MULT = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'
t_ASIGNAR = r'='
#t_IGUAL = r'='

# Otras Expresiones
#t_PUNTOCOMA = ';'
t_PARIZQ = r'\('
t_PARDER = r'\)'




def t_sin(t):
    r'sin'
    return t

def t_cos(t):
    r'cos'
    return t

def t_tan(t):
    r'tan'
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFICADOR(t):
    r'\w+(_\d\w)*'
    return t

def t_CADENA(t):
   r'\"?(\w+ \ *\w*\d* \ *)\"?'
   return t


def t_PLUSPLUS(t):
    r'\+\+'
    return t

def t_DISTINTO(t):
    r'!='
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")

def t_comments_ONELine(t):
     r'\/\/(.)*\n'
     t.lexer.lineno += 1
     print("Comentario de una linea")
t_ignore =' . \t'
#def t_IDENTIFICADOR(t):
#    r'\w+(_\d\w)*'
#    return t

#def t_newline(t):
#   r'\n+'
#  t.lexer.lineno += len(t.value)

def t_error( t):
    global resultado_lexema
    # estado = "** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value),
                                                                    #   str(t.lexpos))
    resultado_lexema.append({
            'line': t.lineno, 
            'type':  str(t.type),
            'value': '** Token no valido = ' + str(t.value),
            'position': t.lexpos,
            'ok': False})
    t.lexer.skip(1)

def prueba(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        resultado_lexema.append({
            'line': tok.lineno, 
            'type':  str(tok.type),
            'value': str(tok.value),
            'position': tok.lexpos,
            'ok': True
        })
    return resultado_lexema


 # instanciamos el analizador lexico
analizador = lex.lex()