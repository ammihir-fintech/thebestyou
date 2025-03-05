
#__init__.py
from flask import Blueprint

# Create a "parent" blueprint for the entire routes package
routes_bp = Blueprint("routes_bp", __name__)



def register_blueprints():
    from .auth import auth_bp  # Import inside the function to avoid circular dependencies
    routes_bp.register_blueprint(auth_bp, url_prefix="/auth") # Import individual blueprints from within the routes folder

# Call Function to register
register_blueprints() 