'''
Minerals: Nafiyu Murtaza, Ben Rudinski, Chloe Wong, Vedant Kothari
SoftDev
P00: Move Slowly and Fix Things
2024-10-31
Time Spent: 1.9
'''

import sqlite3
import hmac
from hashlib import sha256
from app import app

def init_db():
    with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
        cursor = conn.cursor()
        # Create user table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        
        # Create blog_post table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS blog_post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            article TEXT NOT NULL,
            author_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(author_id) REFERENCES user(id)
        )''')
        conn.commit()

class User:
    @staticmethod
    def get_by_username(username):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                return User(*user_data)
            return None

    @staticmethod
    def create(username, password):
        hashed_password = User.hash_password(password)
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()

    @staticmethod
    def verify_password(stored_password, provided_password):
        return hmac.compare_digest(stored_password, User.hash_password(provided_password))

    @staticmethod
    def hash_password(password):
        return sha256(password.encode()).hexdigest()

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class BlogPost:

    # Create a new blog post
    @staticmethod
    def create(category, article, author_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO blog_post (category, article, author_id) VALUES (?, ?, ?)", (category, article, author_id))
            conn.commit()

    # Fetch blog posts by category
    @staticmethod
    def get_by_category(category):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blog_post WHERE category = ? ORDER BY created_at DESC", (category,))
            return cursor.fetchall()

    # Fetch all recent blog posts
    @staticmethod
    def get_recent():
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blog_post ORDER BY created_at DESC")
            return cursor.fetchall()

    # Fetch blog post by ID
    @staticmethod
    def get(post_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blog_post WHERE id = ?", (post_id,))
            return cursor.fetchone()

    # Update an existing blog post
    @staticmethod
    def update(post_id, category, article):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE blog_post SET category = ?, article = ? WHERE id = ?", (category, article, post_id))
            conn.commit()

    # Delete a blog post
    @staticmethod
    def delete(post_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blog_post WHERE id = ?", (post_id,))
            conn.commit()
