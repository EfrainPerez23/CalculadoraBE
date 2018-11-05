import ply.lex as lex
from flask_restful import Resource, reqparse
from Util.BodyParser import BodyParser

# resultado del analisis
resultado_lexema = []

with open('./assets/palabrasReservadas.txt') as f:
    reservadas = f.readlines()
reservadas = [x.strip() for x in reservadas] 
reservada = ()

for reserv in reservadas:
    reservada = reservada + (reserv,)
# reservada = (
#     # Palabras Reservadas
#     'INCLUDE',
#     'USING',
#     'NAMESPACE',
#     'STD',
#     'COUT',
#     'CIN',
#     'GET',
#     'CADENA',
#     'RETURN',
#     'VOID',
#     'INT',
#     'ENDL',
# )

with open('./assets/tokens.txt') as t:
    tkns = t.readlines()
tkns = [x.strip() for x in tkns] 

auxTokens = ()
for atk in tkns:
    auxTokens = auxTokens + (atk,)

tokens = reservada + auxTokens

# tokens = reservada + (
#     'IDENTIFICADOR',
#     'ENTERO',
#     'ASIGNAR',

#     'SUMA',
#     'RESTA',
#     'MULT',
#     'DIV',
#     'POTENCIA',
#     'MODULO',

#    'MINUSMINUS',
#    'PLUSPLUS',

#     #Condiones
#    'SI',
#     'SINO',
#     #Ciclos
#    'MIENTRAS',
#    'PARA',
#     #logica
#     'AND',
#     'OR',
#     'NOT',
#     'MENORQUE',
#     'MENORIGUAL',
#     'MAYORQUE',
#     'MAYORIGUAL',
#     'IGUAL',
#     'DISTINTO',
#     # Symbolos
#     'NUMERAL',

#     'PARIZQ',
#     'PARDER',
#     'CORIZQ',
#     'CORDER',
#     'LLAIZQ',
#     'LLADER',
    
#     # Otros
#     'PUNTOCOMA',
#     'COMA',
#     'COMDOB',
#     'MAYORDER', #>>
#     'MAYORIZQ', #<<
# )

# Reglas de Expresiones Regualres para token de Contexto simple

t_SUMA = r'\+'
t_RESTA = r'-'
t_MINUSMINUS = r'\-\-'
# t_PUNTO = r'\.'
t_MULT = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'

t_ASIGNAR = r'='
# Expresiones Logicas
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_PUNTOCOMA = ';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'
t_COMDOB = r'\"'



def t_INCLUDE(t):
    r'include'
    return t

def t_USING(t):
    r'using'
    return t

def t_NAMESPACE(t):
    r'namespace'
    return t

def t_STD(t):
    r'std'
    return t

def t_COUT(t):
    r'cout'
    return t

def t_CIN(t):
    r'cin'
    return t

def t_GET(t):
    r'get'
    return t

def t_ENDL(t):
    r'endl'
    return t

def t_SINO(t):
    r'else'
    return t

def t_SI(t):
    r'if'
    return t

def t_RETURN(t):
   r'return'
   return t

def t_VOID(t):
   r'void'
   return t

def t_MIENTRAS(t):
    r'while'
    return t

def t_PARA(t):
    r'for'
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

def t_NUMERAL(t):
    r'\#'
    return t

def t_PLUSPLUS(t):
    r'\+\+'
    return t

def t_MENORIGUAL(t):
    r'<='
    return t

def t_MAYORIGUAL(t):
    r'>='
    return t

def t_IGUAL(t):
    r'=='
    return t

def t_MAYORDER(t):
    r'<<'
    return t

def t_MAYORIZQ(t):
    r'>>'
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

# Prueba de ingreso
def prueba(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        # estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos) )
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

# if __name__ == '__main__':
#     while True:
#         data = input("ingrese: ")
#         prueba(data)
#         print(resultado_lexema)
    
class CalculatorResource(Resource):
    
    def post(self):
        data = BodyParser.bodyParser([
            {
                'key': 'data',
                '_type': str,
                '_required': True,
                '_help': 'This field cannot be blank!'
            }
        ])
        prueba(data['data'])
        return {'data': resultado_lexema}