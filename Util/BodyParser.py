
from flask_restful import reqparse

class BodyParser:

    #metodo que crea el parser encargado de validar el cuerpo del json de los request
    @classmethod
    def bodyParser(cls, _args):
        parser = reqparse.RequestParser()
        for _arg in _args:
            parser.add_argument(_arg['key'],
                                type=_arg['_type'],
                                required=_arg['_required'],
                                help=_arg['_help'])
        return parser.parse_args()