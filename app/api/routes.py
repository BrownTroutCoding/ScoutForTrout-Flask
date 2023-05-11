from flask import Blueprint, request, jsonify, render_template, Response
# from helpers import token_required
from models import db, User, FishingLocation, fishing_location_schema, all_locations_schema
from .cfs import get_and_groom_cfs
from .temperature import get_and_groom_temp
# from models import GoogleMapPin, google_map_pin_schema, GoogleMapPinSchema
from flask import g, Flask
from ..authentication.routes import load_user
from flask_cors import CORS
from flask_login import current_user


api = Blueprint('api',__name__,url_prefix='/api')

# Get Data
@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

# Create
@api.route('/fishinglocations/<string:user_id>',methods=['POST'])
@load_user
def add_fishing_location():
    print(request.headers)
    print(request.get_json())
    data = request.get_json()
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid content type'}), 400
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    id = data['id']
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    description = data['description']
    user_id = g.current_user.id

    # Check if id is already in database
    fishing_location = FishingLocation.query.get(id)
    if fishing_location is None:
        fishing_location = FishingLocation(id=id, name=name, latitude=latitude, longitude=longitude, description=description, user_id=user_id)
    else:
        fishing_location.name = name
        fishing_location.latitude = latitude
        fishing_location.longitude = longitude
        fishing_location.description = description
        fishing_location.user_id = user_id

    db.session.add(fishing_location)
    db.session.commit()

    response = fishing_location_schema.dump(fishing_location)
    return jsonify(response), 201, {'Content-Type': 'application/json'}

@api.route('/fishinglocations/<string:user_id>', methods=['GET'])
@load_user
def get_all_locations(user_id):
    user_id = g.current_user.id
    get_all_locations = FishingLocation.query.filter_by(user_id=user_id).all()
    response = all_locations_schema.dump(get_all_locations)
    return jsonify(response)
    
# Retrieve single fishing_location
@api.route('/fishing_location/<string:user_id>',methods=['GET'])
# @load_user
def get_fishing_location(id):
    fishing_location = FishingLocation.query.get(id)
    response = fishing_location_schema.dump(fishing_location)
    return jsonify(response)

#Update fishing_location
@api.route('/fishing_locations/<string:user_id>',methods=["POST", "PUT"])
@load_user
def update_fishing_location(id):
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid content type'}), 400
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    fishing_location = FishingLocation.query.get(id)
    fishing_location.name = data['name']
    fishing_location.latitude = data['latitude']
    fishing_location.longitude = data['longitude']
    fishing_location.description = data['description']
    fishing_location.user_id = g.current_user.id

    db.session.commit()
    response = fishing_location_schema.dump(fishing_location)
    return jsonify(response)


#Delete fishing_location
@api.route('/fishing_locations/<string:user_id>',methods=["DELETE"])
@load_user
def delete_fishing_location(id):
    fishing_location = FishingLocation.query.get(id)
    db.session.delete(fishing_location)
    db.session.commit()

    response = fishing_location_schema.dump(fishing_location)
    return jsonify(response)

@api.route('/cfs/<river_name>')
def get_cfs(river_name):
    cfs_data = get_and_groom_cfs(river_name)
    return jsonify(cfs_data)

@api.route('/temperature/<river_name>')
def get_temp(river_name):
    temp_data = get_and_groom_temp(river_name)
    return jsonify(temp_data)

# @api.route('/google_map_pin', methods=['POST'])
# def add_google_map_pin():
#     data = request.get_json()
#     user_token = data['user_token']
#     fishing_location_id = data['fishing_location_id']
#     latitude = data['latitude']
#     longitude = data['longitude']
#     new_pin = GoogleMapPin(user_token=user_token, fishing_location_id=fishing_location_id, latitude=latitude, longitude=longitude)
#     db.session.add(new_pin)
#     db.session.commit()
#     return google_map_pin_schema.jsonify(new_pin)