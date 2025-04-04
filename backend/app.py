

# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from db_models import db
#from routes.auth import auth_bp
from routes import routes_bp
from flask_cors import CORS
from waitress import serve

import os



def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000",
                        "https://bestyou-three.vercel.app"],  # Add your React app's URL

            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type","Authorization"]
        }
    })
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
    # with app.app_context():
    #     db.create_all()  # Creates SQLite tables if they do not exist
    print("Starting the Flask application...")

    if os.getenv('ENVIRONMENT') == 'production':
        port = int(os.getenv('PORT', 5000))
        #app.run(host='0.0.0.0', port=port)
        serve(app, host='0.0.0.0', port=port)
    else:
        #app.run(debug=True)  # 
        serve(app, host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
