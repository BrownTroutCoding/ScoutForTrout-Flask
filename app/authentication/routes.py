from models import User, db
from flask import Blueprint, request, jsonify, render_template, g, make_response
from flask_cors import CORS
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
import requests
from helpers import token_required
from flask import make_response

auth = Blueprint('auth', __name__, template_folder='auth_templates', url_prefix='/auth')
CORS(auth)


# Fetch Google public keys
response = requests.get('https://www.googleapis.com/oauth2/v3/certs')
public_keys = response.json()

@auth.route('/token', methods=['POST'])
def get_token():
    id_token_str = request.json.get('id_token')

    if not id_token_str:
        return jsonify({'message': 'ID token is required'}), 400

    try:
        # Verify the ID token
        req = g_requests.Request()
        decoded_token = id_token.verify_firebase_token(id_token_str, req)

        # ID token is valid, extract the user's email
        user_email = decoded_token['email']

        # Check if user exists in the database
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'message': 'User does not exist'}), 401

        return jsonify({'token': user.token}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 401

def load_user(token):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = User.query.filter_by(token=token).first()
            if not user:
                return jsonify({'message': 'User not found'}), 404
            g.current_user = user
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth.route('/userdata', methods=['GET'])
@token_required
def get_user_data(current_user_token):
    user_data = {
        "id": current_user_token.id,
        "token": current_user_token.token,
    }
    response = make_response(jsonify(user_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up.html')

    if request.method == 'POST':
        data = request.json
        # print(data)
        email = data.get('email')
        id_token_str = data.get('id_token')

        if not email or not id_token_str:
            return jsonify({'message': 'Email and ID token are required'}), 400

        try:
            # Verify the ID token
            req = g_requests.Request()
            decoded_token = id_token.verify_firebase_token(id_token_str, req)

            # ID token is valid, extract the user's email
            user_email = decoded_token['email']

            if user_email != email:
                raise ValueError('Email does not match ID token email.')

        except ValueError as e:
            return jsonify({'message': str(e)}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            response = jsonify({'message': 'User already exists', 'token': existing_user.token})
            return response, 409

        # Create new user and save ID token
        user = User(email=email, g_auth_verify=True) # Set g_auth_verify to True
        db.session.add(user)
        db.session.commit()

        response = jsonify({'message': 'User created successfully', 'id': user.id, 'token': user.token})
        return response, 201


# simulate login route
@auth.route('/simulate-login')
def simulate_login():
    return render_template('simulate_login.html')

