# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

#inialize our flask app and config
app = Flask(__name__)
app.config.from_object(Config)

# initialize our database of sql alchemy
db = SQLAlchemy(app)

# import our routes and models for the app
from app import routes, models




