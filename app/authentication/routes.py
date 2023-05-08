from models import User, db, login_manager
from flask import Blueprint, request, jsonify, render_template
from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
import requests
from flask_login import login_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# Fetch Google public keys
response = requests.get('https://www.googleapis.com/oauth2/v3/certs')
public_keys = response.json()

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up.html')

    data = request.json
    print(data)
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
        return jsonify({'message': 'User already exists'}), 409

    # Create new user and save ID token
    user = User(email=email)
    db.session.add(user)
    db.session.commit()

    # After creating the user
    login_user(user)

    return jsonify({'message': 'User created successfully'}), 201


@login_manager.request_loader
def load_user_from_request(request):
    # Attempt to extract the ID token from the request's Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        id_token_str = auth_header[7:]
        try:
            req = g_requests.Request()
            decoded_token = id_token.verify_firebase_token(id_token_str, req)
            user_email = decoded_token['email']
            user = User.query.filter_by(email=user_email).first()
            return user
        except ValueError as e:
            return None
    return None


# simulate login route
@auth.route('/simulate-login')
def simulate_login():
    return render_template('simulate_login.html')