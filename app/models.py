'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: 1
'''

from app import db
from flask_login import UserMixin
import sqlite3

# init db and create tables
def init_db():
    with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
        friend = conn.cursor()

        # user table
        friend.execute('''CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')

        # BlogPost table
        friend.execute('''CREATE TABLE IF NOT EXISTS blog_post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            article TEXT NOT NULL,
            author_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES user(id)
        )''')

        friend.commit()

class User(UserMixin):
    @staticmethod
    def get_by_username(username):
        with sqlite3.connect(app.config['DATABASE.PATH']) as conn:
            friend = conn.cursor()
            friend.execute("SELECT * FROM user WHERE username = ?", (username,))
            return friend.fetchone()

    @staticmethod
    def create(username, password):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
            friend.commit()

    @staticmethod
    def get(user_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("SELECT * FROM user WHERE id = ?", (user_id,))
            return friend.fetchone()

# BlogPost model for db
class BlogPost:
    @staticmethod
    def create(category, article, author_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("INSERT INTO blog_post (category, article, author_id) VALUES (?, ?, ?)", (category, article, author_id))
            friend.commit()