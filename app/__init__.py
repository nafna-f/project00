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
from config import Config

#inialize our flask app and config
app = Flask(__name__)
app.config.from_object(Config)

# initialize our database of sql alchemy
db = SQLAlchemy(app)

# import our routes and models for the app
from app import routes, models




