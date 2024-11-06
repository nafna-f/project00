'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: .3
'''

# imports
from flask import Flask
from config import Config
from flask_simplelogin import SimpleLogin

# initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# user validation logic
def validate_user(username, password):
    from app.models import User # avoid circular imports
    user = User.get_by_username(username)
    if user and User.verify_password(user.password, password):
        return True  # success
    return False

# init login
SimpleLogin(app)

# import routes after app initialization
from app import routes




