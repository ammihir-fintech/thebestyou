

# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from db_models import db
#from routes.auth import auth_bp
from routes import routes_bp


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thebestyou.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(routes_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Creates SQLite tables if they do not exist
    print("Starting the Flask application...")
    app.run(debug=True)
