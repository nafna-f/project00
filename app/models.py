'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: 1.2
'''

from app import app
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

        # BlogPost table with created_at column for timestamps
        friend.execute('''CREATE TABLE IF NOT EXISTS blog_post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            article TEXT NOT NULL,
            author_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  # ADDED CREATED_AT COLUMN FOR TIMESTAMP
            FOREIGN KEY(author_id) REFERENCES user(id)
        )''')

        conn.commit()

class User(UserMixin):

    # get user by usrnmae
    @staticmethod
    def get_by_username(username):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("SELECT * FROM user WHERE username = ?", (username,))
            return friend.fetchone()

    # create user
    @staticmethod
    def create(username, password):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

    # get by user id
    @staticmethod
    def get(user_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("SELECT * FROM user WHERE id = ?", (user_id,))
            return friend.fetchone()

# BlogPost model for db
class BlogPost:

    # create blogpost
    @staticmethod
    def create(category, article, author_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("INSERT INTO blog_post (category, article, author_id) VALUES (?, ?, ?)", (category, article, author_id))
            conn.commit()

    # get blog post by category
    @staticmethod
    def get_by_category(category):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("SELECT * FROM blog_post WHERE category = ? ORDER BY created_at DESC", (category,))  # ADDED ORDER BY CREATED_AT DESC FOR RECENT POSTS FIRST
            return friend.fetchall()
    
    # get all blog posts, most recent first
    @staticmethod
    def get_recent():
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("SELECT * FROM blog_post ORDER BY created_at DESC")  # order for most recent first
            return friend.fetchall()
        
    # get by post id
    @staticmethod
    def get(post_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("SELECT * FROM blog_post WHERE id = ?", (post_id,))
            return friend.fetchone()

    # update post 
    @staticmethod
    def update(post_id, category, article):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("UPDATE blog_post SET category = ?, article = ? WHERE id = ?", (category, article, post_id))
            conn.commit()

    # del post 
    @staticmethod
    def delete(post_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            friend = conn.cursor()
            friend.execute("DELETE FROM blog_post WHERE id = ?", (post_id,))
            conn.commit()
