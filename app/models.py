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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Create blog_post table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blog_post (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                author_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(author_id) REFERENCES user(id)
            )
        ''')
        
        # Check existing columns in blog_post table
        cursor.execute("PRAGMA table_info(blog_post);")
        columns = [info[1] for info in cursor.fetchall()]
        
        # Add 'title' column if it doesn't exist
        if 'title' not in columns:
            cursor.execute("ALTER TABLE blog_post ADD COLUMN title TEXT;")
        
        # Add 'content' column if it doesn't exist
        if 'content' not in columns:
            cursor.execute("ALTER TABLE blog_post ADD COLUMN content TEXT;")
        
        # Commit changes
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
        hashed_password = User.hash_password(password)  # Hashing once during registration
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()

    @staticmethod
    def verify_password(stored_password, provided_password):
        hashed_provided_password = User.hash_password(provided_password)  # Hashing provided password once
        return hmac.compare_digest(stored_password, hashed_provided_password)

    @staticmethod
    def hash_password(password):
        hashed_password = sha256(password.encode()).hexdigest()
        return hashed_password
    
    @staticmethod
    def get_by_id(user_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(*user_data)
            return None
        
    @staticmethod
    def get(user_id):
        return User.get_by_id(user_id)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class BlogPost:
    # Create a new blog post
    @staticmethod
    def create(category, title, content, author_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO blog_post (category, title, content, author_id) VALUES (?, ?, ?, ?)", (category, title, content, author_id))
            conn.commit()

    # Fetch blog posts by category
    @staticmethod
    def get_by_category(category):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blog_post WHERE category = ? ORDER BY created_at DESC", (category,))
            rows = cursor.fetchall()
            return [BlogPost(**row) for row in rows]

    # Fetch all recent blog posts
    @staticmethod
    def get_recent():
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT blog_post.*, user.username 
                FROM blog_post 
                JOIN user ON blog_post.author_id = user.id 
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            return [BlogPost(**row) for row in rows]

    # Fetch blog post by ID
    @staticmethod
    def get(post_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            conn.row_factory = sqlite3.Row  # This allows us to access columns by name
            cursor = conn.cursor()
            cursor.execute("""
                SELECT blog_post.*, user.username 
                FROM blog_post 
                JOIN user ON blog_post.author_id = user.id 
                WHERE blog_post.id = ?
            """, (post_id,))
            row = cursor.fetchone()
            if row:
                return BlogPost(**row)
            else:
                return None

    # Update an existing blog post
    @staticmethod
    def update(post_id, category, title, content):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE blog_post SET category = ?, title = ?, content = ? WHERE id = ?", (category, title, content, post_id))
            conn.commit()

    # Delete a blog post
    @staticmethod
    def delete(post_id):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blog_post WHERE id = ?", (post_id,))
            conn.commit()

    @staticmethod
    def get_all():
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT blog_post.*, user.username 
                FROM blog_post 
                JOIN user ON blog_post.author_id = user.id 
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            return [BlogPost(**row) for row in rows]

    @staticmethod
    def search(query):
        with sqlite3.connect(app.config['DATABASE_PATH']) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = f"%{query}%"
            cursor.execute("""
                SELECT blog_post.*, user.username 
                FROM blog_post 
                JOIN user ON blog_post.author_id = user.id 
                WHERE blog_post.title LIKE ? OR blog_post.content LIKE ? OR user.username LIKE ?
                ORDER BY created_at DESC
            """, (query, query, query))
            rows = cursor.fetchall()
            return [BlogPost(**row) for row in rows]

    def __init__(self, id, title, content, category, author_id, created_at, username=None):
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.author_id = author_id
        self.created_at = created_at
        self.username = username  # Author's username
