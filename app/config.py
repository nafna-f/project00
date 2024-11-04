'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: .1
'''

import os

class Config: 
    # secret key for securely using session cookie
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'Minerals'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db' # will change later for name of db
    SQLALCHEMY_TRACK_MODIFICATIONS = False # disable tracking notifications ofr better performance