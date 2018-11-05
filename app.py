
from flask import Flask, jsonify
from flask_restful import Api

# Resources
from Resources.analizador_sintactico import CalculatorResource

app = Flask(__name__)


# Load config File
app.secret_key = 'calculator'

# Init Rest API endpoints
api = Api(app)
api.add_resource(CalculatorResource, '/calculate')

# Main function
if __name__ == '__main__':
    app.run(debug=True)