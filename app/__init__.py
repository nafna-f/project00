'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: .9
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
    from app.models import User  # Import inside to avoid circular imports
    user = User.get_by_username(username)
    if user:
        print("User found in database.")  # Debug message
        if User.verify_password(user.password, password):
            print("Password verified.")  # Debug message
            return True
        else:
            print("Password verification failed.")  # Debug message
    else:
        print("User not found.")  # Debug message
    return False


# init login
SimpleLogin(app, login_checker=validate_user)

# import routes after app initialization
from app import routes

# set up the database when the app context is available
with app.app_context():
    from app.models import init_db
    init_db()





