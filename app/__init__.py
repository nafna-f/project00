'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: .3
'''

# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

#inialize our flask app and config
app = Flask(__name__)
app.config.from_object(Config)

# initialize our database of sql alchemy
db = SQLAlchemy(app)

#loginmanager for session handling
login_manager = LoginManager(app)
login_manager.login_view = 'login' # redirect user to login page if not logged in
login_manager.login_message_category = 'info' # typ of msg shown

# import our routes and models for the app
from app import routes, models




