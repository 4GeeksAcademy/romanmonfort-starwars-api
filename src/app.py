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
from models import db, User,Planet,Character,Vehicle,Favorite
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

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_hello(user_id):
    users = User.query.get(user_id)
    serialized_users= users.serialize()
    return jsonify({'msg':"ok","result":serialized_users}), 200

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify({'msg': "ok", 'result': serialized_users}), 200

@app.route('/user', methods=['POST'])
def post_users():
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    if "email" not in body or "password" not in body or "is_active" not in body:
        return jsonify({'msg': 'Los campos email, password y is_active son obligatorios'}), 400

    new_user = User(email=body['email'], password=body['password'], is_active=body['is_active'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': "Usuario creado exitosamente"}), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    if "email" in body:
        user.email = body['email']
    if "password" in body:
        user.password = body['password']
    if "is_active" in body:
        user.is_active = body['is_active']

    db.session.commit()

    return jsonify({'msg': 'Usuario actualizado ', 'user': user.serialize()}), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg': 'Usuario eliminado exitosamente'}), 200








@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify({'msg': "ok", 'result': serialized_planets}), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet:
        serialized_planet = planet.serialize()
        return jsonify({'msg': "ok", 'result': serialized_planet}), 200
    else:
        return jsonify({'msg': "Planet not found", 'result': {}}), 404

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({'msg': 'Debes proporcionar el nombre del planeta'}), 400

    new_planet = Planet(name=data['name'], population=data.get('population'))

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({'msg': 'Planeta creado exitosamente', 'planet': new_planet.serialize()}), 200


@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({'msg': 'Planeta no encontrado'}), 404

    # Actualiza los campos si están presentes en el cuerpo de la solicitud
    if "name" in body:
        planet.name = body['name']
    if "population" in body:
        planet.population = body['population']

    db.session.commit()

    return jsonify({'msg': 'Planeta actualizado exitosamente', 'planet': planet.serialize()}), 200




@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({'msg': 'Planeta no encontrado'}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({'msg': 'Planeta eliminado exitosamente'}), 200















@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify({'msg': "ok", 'result': serialized_characters}), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    
    if character:
        serialized_character = character.serialize()
        return jsonify({'msg': "ok", 'result': serialized_character}), 200
    else:
        return jsonify({'msg': "Character not found", 'result': {}}), 404

@app.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()

    if not data or "name" not in data or "planet_id" not in data:
        return jsonify({'msg': 'Debes proporcionar  el nombre del personaje y el ID del planeta de donde viene'}), 400

    new_character = Character(
        name=data['name'],
        height=data.get('height'),
        mass=data.get('mass'),
        planet_id=data['planet_id']
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify({'msg': 'Personaje creado exitosamente', 'character': new_character.serialize()}), 201

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)

    if not character:
        return jsonify({'msg': 'Personaje no encontrado'}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({'msg': 'Personaje eliminado exitosamente'}), 200

@app.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    character = Character.query.get(character_id)

    if not character:
        return jsonify({'msg': 'Personaje no encontrado'}), 404

    # Actualiza los campos si están presentes en el cuerpo de la solicitud
    if "name" in body:
        character.name = body['name']
    if "height" in body:
        character.height = body['height']
    if "mass" in body:
        character.mass = body['mass']
    if "planet_id" in body:
        character.planet_id = body['planet_id']

    db.session.commit()

    return jsonify({'msg': 'Personaje actualizado exitosamente', 'character': character.serialize()}), 200












@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]
    return jsonify({'msg': "ok", 'result': serialized_vehicles}), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    
    if vehicle:
        serialized_vehicle = vehicle.serialize()
        return jsonify({'msg': "ok", 'result': serialized_vehicle}), 200
    else:
        return jsonify({'msg': "Vehicle not found", 'result': {}}), 404
    


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()

    if not data or "name" not in data or "type" not in data:
        return jsonify({'msg': 'Debes proporcionar el nombre del vehículo y el tipo'}), 400

    new_vehicle = Vehicle(
        name=data['name'],
        type=data['type']
    )

    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify({'msg': 'Vehículo creado exitosamente', 'vehicle': new_vehicle.serialize()}), 201



@app.route('/vehicle/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({'msg': 'Debes enviar información en el body'}), 400

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({'msg': 'Vehículo no encontrado'}), 404

    # Actualiza los campos si están presentes en el cuerpo de la solicitud
    if "name" in body:
        vehicle.name = body['name']
    if "type" in body:
        vehicle.type = body['type']

    db.session.commit()

    return jsonify({'msg': 'Vehículo actualizado exitosamente', 'vehicle': vehicle.serialize()}), 200



@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({'msg': 'Vehículo no encontrado'}), 404

    db.session.delete(vehicle)
    db.session.commit()

    return jsonify({'msg': 'Vehículo eliminado exitosamente'}), 200



@app.route('/favorites/user/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorites_serialize = []

    for favorite_item in favorites:
        favorites_serialize.append({'favorite': favorite_item.serialize()})

    return jsonify({'msg': 'ok', 'result': favorites_serialize, 'user': user.serialize()}), 200

@app.route('/favorites/user/<int:user_id>/add', methods=['POST'])
def add_favorite(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'msg': 'El usuario no existe'}), 404

    data = request.get_json()

    if not data or 'type' not in data or 'item_id' not in data:
        return jsonify({'msg': 'Datos no válidos en el cuerpo de la solicitud'}), 400

    type = data['type']
    item_id = data['item_id']

    if type not in ['planet', 'vehicle', 'character']:
        return jsonify({'msg': 'Tipo no válido'}), 400

    new_favorite = Favorite(user_id=user_id)

    if type == 'planet':
        new_favorite.planet_id = item_id
    elif type == 'vehicle':
        new_favorite.vehicle_id = item_id
    elif type == 'character':
        new_favorite.character_id = item_id

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'msg': 'Favorito creado exitosamente'}), 201


@app.route('/favorites/user/<int:user_id>/remove', methods=['DELETE'])
def remove_favorite(user_id):
    user = User.query.get(user_id)
    
    data = request.get_json()

    if not data or 'favorite_id' not in data:
        return jsonify({'msg': 'Datos no válidos en el cuerpo de la solicitud'}), 400

    favorite_id = data['favorite_id']
    favorite = Favorite.query.get(favorite_id)

    if user is None or favorite is None or favorite.user_id != user_id:
        return jsonify({'msg': 'El usuario o el favorito no existen'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'msg': 'Favorito eliminado exitosamente'}), 200

@app.route('/favorites/all', methods=['GET'])
def get_all_favorites():
    all_favorites = Favorite.query.all()

    all_favorites_serialize = []

    for favorite_item in all_favorites:
        all_favorites_serialize.append({'favorite': favorite_item.serialize()})

    return jsonify({'msg': 'ok', 'result': all_favorites_serialize}), 200

















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
