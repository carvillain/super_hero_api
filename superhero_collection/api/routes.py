from flask import Blueprint, json, request, jsonify
from superhero_collection.helpers import token_required
from superhero_collection.models import Super, db, User, super_schema, supers_schema

api = Blueprint('api', __name__, url_prefix= '/api')

@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return {'some': 'value'}

# Create Super Endpoint
@api.route('/supers', methods = ['POST'])
@token_required
def create_super(current_user_token):
    name = request.json['name']
    description = request.json['description']
    universe = request.json['universe']
    hero_or_villain = request.json['hero_or_villain']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    super = Super(name, description, universe, hero_or_villain, comics_appeared_in, super_power, user_token)

    db.session.add(super)
    db.session.commit()

    response = super_schema.dump(super)
    return jsonify(response)

# Retrieve All Supers Endpoint
@api.route('/supers', methods = ['GET'])
@token_required
def get_supers(current_user_token):
    owner = current_user_token.token
    supers = Super.query.filter_by(user_token = owner).all()
    response = supers_schema.dump(supers)
    return jsonify(response)

# Retrieve One Super Endpoint
@api.route('/supers/<id>', methods = ['GET'])
@token_required
def get_super(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        super = Super.query.get(id)
        response = super_schema.dump(super)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# Update Super Endpoint
@api.route('/supers/<id>', methods = ['POST', 'PUT'])
@token_required
def update_super(current_user_token, id):
    super = Super.query.get(id) # Get Super Instance

    super.name = request.json['name']
    super.description = request.json['description']
    super.universe = request.json['universe']
    super.hero_or_villain = request.json['hero_or_villain']
    super.comics_appeared_in = request.json['comics_appeared_in']
    super.super_power = request.json['super_power']
    super.user_token = current_user_token.token

    db.session.commit()
    response = super_schema.dump(super)
    return jsonify(response)

# Delete Super Instance
@api.route('/supers/<id>', methods = ['DELETE'])
@token_required
def delete_super(current_user_token, id):
    super = Super.query.get(id)
    db.session.delete(super)
    db.session.commit()

    response = super_schema.dump(super)
    return jsonify(response)