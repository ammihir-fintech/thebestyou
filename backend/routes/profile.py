from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db_models import db, Profile, User

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/create", methods=["POST"])
@jwt_required()  # Requires a valid token
def create_profile():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get logged-in user's ID

    # Check if user already has a profile
    if Profile.query.filter_by(user_id=user_id).first():
        return jsonify({"error": "Profile already exists"}), 400

    # Extract profile details from request
    name = data.get("name")
    age = data.get("age")
    bio = data.get("bio")
    interests = data.get("interests")
    

    # Validate required fields
    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    # Create profile record
    new_profile = Profile(
        user_id=user_id,
        name=name,
        age=age,
        bio=bio,
        interests=interests,
        
    )

    db.session.add(new_profile)
    db.session.commit()

    return jsonify({"message": "Profile created successfully", "profile_id": new_profile.id}), 201

@profile_bp.route("/view", methods=["GET"])
@jwt_required()
def view_profile():
    user_id = get_jwt_identity()
    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "No profile found"}), 404

    return jsonify({
        "name": profile.name,
        "age": profile.age,
        "bio": profile.bio,
        "interests": profile.interests,
        
    }), 200
