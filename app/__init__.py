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

# Set up the database when the app context is available
with app.app_context():
    from app.models import init_db
    init_db()

# Import routes after app initialization
from app import routes

