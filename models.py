from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# 1. User Model (For Login/Signup Feature)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# 2. Movie Model (For Movie Portal & Cinema Finder)
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    poster_image = db.Column(db.String(100), nullable=False) # Holds filename like 'inception.jpg'