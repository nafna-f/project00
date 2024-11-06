# setup_db.py
from app import app
from app.models import init_db

with app.app_context():
    init_db()
