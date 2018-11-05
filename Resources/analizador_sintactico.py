import ply.yacc as yacc
import math
from Resources.analizador_lexico import tokens, prueba
from Util.BodyParser import BodyParser
from flask_restful import Resource, reqparse

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right', 'IDENTIFICADOR'),
    ('right', 'ASIGNAR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('left', 'POTENCIA', 'MODULO'),
    ('right', 'sin', 'cos', 'tan'),
    ('left', 'PARIZQ', 'PARDER'),

)
nombres = {}

def p_declaracion_igual(t):
   '''declaracion : IDENTIFICADOR ASIGNAR expresion'''
   nombres[t[1]] = t[3]

def p_declaracion_expr(t):
    'declaracion : expresion'
    # print("Resultado: " + str(t[1]))
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion   :   expresion SUMA expresion
                |   expresion RESTA expresion
                |   expresion MULT expresion
                |   expresion DIV expresion
                |   expresion POTENCIA expresion
                |   expresion MODULO expresion

    '''
    
    if t[2] == '+':
        print(t)
        t[0] = t[1] + t[3]
    elif t[4] == '-':
        t[0] = t[1] - t[3]
    elif t[4] == '*':
        t[0] = t[1] * t[3]
    elif t[4] == '/':
        t[0] = t[1] / t[3]
    elif t[4] == '%':
        t[0] = t[1] % t[3]
    elif t[4] == '**' or t[4] == '^':
        i = t[3]
        t[0] = t[1]
        while i > 1:
            t[0] *= t[1]
            i -= 1

def p_expresion_trig(t):
    '''expresion : sin PARIZQ expresion PARDER
                | cos PARIZQ expresion PARDER
                | tan PARIZQ expresion PARDER'''
    if t[1] == "sin":
        t[0] = math.sin(t[3])
    elif t[1] == "cos":
        t[0] = math.cos(t[3])
    elif t[1] == "tan":
        t[0] = math.tan(t[3])

def p_expresion_grupo(t):
    'expresion  : PARIZQ expresion PARDER'
    t[0] = t[2]


def p_expresion_numero(t):
    'expresion : ENTERO'
    t[0] = t[1]

#def p_expresion_nombre(t):
 #   'expresion : IDENTIFICADOR'
  #  try:
   #     t[0] = nombres[t[1]]
    #except LookupError:
     #   print("Nombre desconocido ", t[1])
      #  t[0] = 0

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {} en el valor {}".format( str(t.type),str(t.value))
        print(resultado)
    else:
        resultado = "Error sintactico {}".format(t)
        print(resultado)
    resultado_gramatica.append(resultado)



# instanciamos el analizador sintactico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    data = data.strip()
    resultado_gramatica.clear()

    for item in data.splitlines():
        if item:
            gram = parser.parse(item)
            if gram:
                resultado_gramatica.append(str(gram))
        else: print("data vacia")

    return resultado_gramatica

        

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
        
        stringToAnalize = data['data'].strip()
        return {'result': prueba_sintactica(stringToAnalize), 'lexico': prueba(stringToAnalize)}

