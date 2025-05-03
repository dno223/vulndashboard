import os

class Config:
    """Configuration class for the Flask application."""
    SECRET_KEY =os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NVD_API_KEY = os.environ.get('NVD_API_KEY') or 'f1d91838-2d6a-43f7-b15e-1cfe30761f6b'
