from models import User, db
from flask import Blueprint, request, jsonify, render_template
from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
import requests


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
    user = User(email=email, id_token=id_token_str)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


# simulate login route
@auth.route('/simulate-login')
def simulate_login():
    return render_template('simulate_login.html')