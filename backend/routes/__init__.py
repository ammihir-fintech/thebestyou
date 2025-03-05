
#__init__.py
from flask import Blueprint

# Create a "parent" blueprint for the entire routes package
routes_bp = Blueprint("routes_bp", __name__)



def register_blueprints():
    from .auth import auth_bp  # Import inside the function to avoid circular dependencies
    from .upload import upload_bp  
    from .profile import profile_bp  

    routes_bp.register_blueprint(auth_bp, url_prefix="/auth") # Import individual blueprints from within the routes folder
    routes_bp.register_blueprint(upload_bp, url_prefix="/upload")
    routes_bp.register_blueprint(profile_bp, url_prefix="/profile")

# Call Function to register
register_blueprints() 