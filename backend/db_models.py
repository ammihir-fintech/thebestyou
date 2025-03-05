

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)



class UploadedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # ID of the user who uploaded the image
    #file_path = db.Column(db.String(256), nullable=False)  # Path where the file is stored
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)  # Time of upload




class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    interests = db.Column(db.Text, nullable=True)
  

    #user = db.relationship("User", backref=db.backref("profile", uselist=False))