import os

class Config:
    # Admin Credentials
    ADMIN_EMAIL = 'admin@example.com'  # Replace with your admin email
    ADMIN_PASSWORD = 'admin123'  # Use environment variables for security

    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')  # Replace 'your_secret_key' with a secure key
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']  # Allow toggling debug mode via environment variables

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///restaurant.db')  # Use DATABASE_URL for flexibility
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance

    # Mail Config
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')  # Default to Gmail's SMTP server
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))  # Default to port 587 for TLS
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']  # Convert to boolean
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'your_email@example.com')  # Replace with your email
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'your_password')  # Replace with your email password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)  # Default sender is the username