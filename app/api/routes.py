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
# @api.route('/getdata')
# def getdata():
#     return {'yee': 'haw'}

# Create
@api.route('/fishinglocations/<string:user_id>',methods=['POST'])
@load_user
def add_fishing_location(user_id):
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
    print(f"User ID: {user_id}")  # Add this line to debug
    get_all_locations = FishingLocation.query.filter_by(user_id=user_id).all()
    response = all_locations_schema.dump(get_all_locations)
    return jsonify(response)


    
# Retrieve single fishing_location
@api.route('/fishinglocations/<string:user_id>',methods=['GET'])
# @load_user
def get_fishing_location(id):
    fishing_location = FishingLocation.query.get(id)
    response = fishing_location_schema.dump(fishing_location)
    return jsonify(response)

#Update fishing_location
@api.route('/fishinglocations/<string:locationId>', methods=['PUT'])
@load_user
def update_fishing_location(locationId):
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid content type'}), 400
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    fishing_location = FishingLocation.query.get(locationId)
    if fishing_location is None:
        return jsonify({'error': 'Fishing location not found'}), 404
    else:
        fishing_location.name = data['name']
        fishing_location.latitude = data['latitude']
        fishing_location.longitude = data['longitude']
        fishing_location.description = data['description']
        fishing_location.user_id = g.current_user.id

        db.session.commit()
        response = fishing_location_schema.dump(fishing_location)
        return jsonify(response), 200, {'Content-Type': 'application/json'}


# Delete fishing_location
@api.route('/fishinglocations/<string:id>', methods=["DELETE"])
@load_user
def delete_fishing_location(id):
    user_id = g.current_user.id
    fishing_location = FishingLocation.query.filter_by(id=id, user_id=user_id).first()
    if fishing_location:
        db.session.delete(fishing_location)
        db.session.commit()
        response = fishing_location_schema.dump(fishing_location)
        return jsonify(response)
    else:
        return jsonify({"message": "Fishing location not found or not authorized to delete"}), 404

@api.route('/cfs/<river_name>', methods=['GET'])
def get_cfs(river_name):
    cfs_data = get_and_groom_cfs(river_name)
    return jsonify(cfs_data)

@api.route('/temp/<river_name>', methods=['GET'])
def get_temp(river_name):
    temp_data = get_and_groom_temp(river_name)
    return jsonify(temp_data)