from models import User, db, check_password_hash
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from werkzeug.security import generate_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'})

@auth.route('/signin', methods=['POST'])
def signin():
    email = request.json['email']
    password = request.json['password']

    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password,password):
        login_user(logged_user)
        return jsonify({'message': 'Login Successful'})
    else:
        return jsonify({'message': 'Invalid email or password'})

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout Successful'})

@auth.route('/update', methods=['PUT'])
@login_required
def update():
    logged_user = User.query.filter_by(id=current_user.id).first()
    if not logged_user:
        return jsonify({'message': 'User not found'})
    
    data = request.get_json()
    logged_user.email = data.get('email', logged_user.email)
    logged_user.password = generate_password_hash(data.get('password')) if data.get('password') else logged_user.password

    db.session.commit()

    return jsonify({'message': 'User updated successfully'})


