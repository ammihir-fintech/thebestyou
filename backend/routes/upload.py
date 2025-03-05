import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
from db_models import db, UploadedImage

upload_bp = Blueprint("upload", __name__)

# Set the folder where uploaded files will be saved
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/image", methods=["POST"]) # 
@jwt_required()
def upload_photo():
    
    

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)  # Secure the filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)  # Save the file to the uploads directory
        
        #Get the current user's ID from the JWT token
        current_user_id = get_jwt_identity()
        #push the upload details to the UploadedImage table
        uploaded_image = UploadedImage(user_id=current_user_id)
        db.session.add(uploaded_image)
        db.session.commit()

        #Placeholder for image analysis

        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 201
    


    return jsonify({"error": "Invalid file type. Allowed types: png, jpg, jpeg, gif"}), 400
