"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Character, Planeta, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    all_usuarios = Usuario.query.all()
    if all_usuarios is not None:
        return jsonify([usuario.serialize() for usuario in all_usuarios]), 200
    else:
        return jsonify({"message": "Error! Users not found! Try again"}), 404

@app.route('/character', methods=['POST'])
def post_character():
    body = request.json

    if 'name' not in body:
        return jsonify({"message": "Error! Asegúrate de enviar 'name' en el body"}), 400
    if 'description' not in body:
        return jsonify({"message": "Error! Asegúrate de enviar 'description' en el body"}), 400
    try:
        new_character = Character(body['name'], body['description'])
        db.session.add(new_character)
        db.session.commit()
        return jsonify(new_character.serialize()), 200

    except Exception as err:
        return jsonify({"message": err}), 500

@app.route('/characters', methods=['GET'])
def get_all_characters():
    all_characters = Character.query.all()
    
    if all_characters is not None:
        return jsonify([character.serialize() for character in all_characters]), 200
    else:
        return jsonify({"message": "Error! Character not found!"}), 404

@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):
    character = Character.query.get(id)

    if character is not None:
        return jsonify(character.serialize()), 200
    else:
        return jsonify({"message": "Error! Character not found!"}), 404

@app.route('/planeta', methods=['POST'])
def post_planeta():
    body = request.json

    if 'name' not in body:
        return jsonify({"message": "Error! Asegúrate de enviar 'name' en el body"}), 400
    if 'description' not in body:
        return jsonify({"message": "Error! Asegúrate de enviar 'description' en el body"}), 400
    try:
        new_planeta = Planeta(body['name'], body['description'])
        db.session.add(new_planeta)
        db.session.commit()
        return jsonify(new_planeta.serialize()), 200

    except Exception as err:
        return jsonify({"message": err}), 500

@app.route('/planetas', methods=['GET'])
def get_all_planetas():
    all_planetas = Planeta.query.all()
    
    if all_planetas is not None:
        return jsonify([planeta.serialize() for planeta in all_planetas]), 200
    else:
        return jsonify({"message": "Error! Planets not found!"}), 404

@app.route('/planeta/<int:id>', methods=['GET'])
def get_one_planeta(id):
    planeta = Planeta.query.get(id)

    if planeta is not None:
        return jsonify(planeta.serialize()), 200
    else: 
        return jsonify({"message": "Error! Planet not found!"}), 404

@app.route('/favorite/planeta/<int:planeta_id>', methods=['POST'])
def add_planeta_favorite(planeta_id):
    body = request.json
    if 'user_id' not in body:
        return jsonify({"message": "Error! User not found!"}), 400
    try:
        new_favorite_planeta = Favorite(None, planeta_id, body['user_id'])
        db.session.add(new_favorite_planeta)
        db.session.commit()
        return jsonify(new_favorite_planeta.serialize()), 200

    except Exception as err:
        return jsonify({"message": err}), 500

@app.route('/favorite/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_favorite_planeta(planeta_id):
    delete_planeta = Favorite.query.filter_by(planeta_id = planeta_id).first()
    if delete_planeta is not None:
        db.session.delete(delete_planeta)
    else:
        return jsonify({"message": "Error! Planet not found!"}), 404
    try:
        db.session.commit()
        response_body={
            "done": True
        }
        return jsonify(response_body), 200
    except Exception as err:
        return jsonify({"message": err}), 500 

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_character_favorite(character_id):
    body = request.json
    if 'user_id' not in body:
        return jsonify({"message": "Error! User not found!"}), 400
    try:
        new_favorite_character = Favorite(character_id, None, body['user_id'])
        db.session.add(new_favorite_character)
        db.session.commit()
        return jsonify(new_favorite_character.serialize()), 200

    except Exception as err:
        return jsonify({"message": err}), 500

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    delete_character = Favorite.query.filter_by(character_id = character_id).first()
    if delete_character is not None:
        db.session.delete(delete_character)
    else:
        return jsonify({"message": "Error! Character not found!"}), 404
    try:
        db.session.commit()
        response_body={
            "done": True
        }
        return jsonify(response_body), 200
    except Exception as err:
        return jsonify({"message": err}), 500 

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_all_favorites(user_id):
    all_user_favorites = Favorite.query.filter_by(user_id = user_id)
    
    if all_user_favorites is not None:
        return jsonify([favorite.serialize() for favorite in all_user_favorites]), 200
    else:
        return jsonify({"message": "Favorites not found"}), 404
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
