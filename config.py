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
    DATABASE_PATH = os.path.join(os.getcwd(), 'site.db') # set db path