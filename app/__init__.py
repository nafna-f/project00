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

# initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Import models and initialize the database within the app context
from app.models import init_db

with app.app_context():
    init_db()  # Call to create tables if they don't already exist

# Import routes after app initialization to avoid circular imports
from app import routes
