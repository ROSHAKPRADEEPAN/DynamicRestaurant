from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# Initialize extensions at the module level
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configuration from config.py

    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)

    # Import and register blueprints after app and extensions are initialized
    from .routes import main  # Import here to avoid circular import
    app.register_blueprint(main)

    # Create database tables if they don't exist
    with app.app_context():
        print("Creating database tables...")  # Debug statement
        db.create_all()
        print("Database tables created.")

    return app