

# auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    unset_jwt_cookies
)
from db_models import User, db

auth_bp = Blueprint('auth', __name__) # name corresponds to the script name

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # Create a new user with a hashed password
    new_user = User(
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create an access token using the user's id as identity
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Logout can be handled client-side by deleting the token.
    # Optionally, implement token blacklisting to invalidate tokens server-side.
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200
