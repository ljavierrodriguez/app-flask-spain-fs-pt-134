from config import Config
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from routes import api

app = Flask(__name__)
app.config.from_object(Config) # Configurando nuestra app desde la clase Config

CORS(app)

# Configuracion con la base de datos (models)
db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)

"""
Comandos Habilitados con Migrate

flask db init
flask db migrate
flask db upgrade 
flask db downgrade
"""

# Vincular Rutas 
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def main():
    return jsonify({ "status": "Server funcionando correctamente!"}), 200

if __name__ == '__main__':
    app.run()