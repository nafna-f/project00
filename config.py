import os

class Config: 
    # secret key for securely using session cookie
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'Minerals'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db' # will change later for name of db
    SQLALCHEMY_TRACK_MODIFICATIONS = False # disable tracking notifications ofr better performance