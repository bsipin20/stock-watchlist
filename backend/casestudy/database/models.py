from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from casestudy.extensions import db

class User(db.Model):
    """Model for a user"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(512))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

class Security(db.Model):
    """Model for a security"""
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(64), unique=True)

class Watchlist(db.Model):
    """Model for a watchlist entry"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'), nullable=False, index=True)

    def __repr__(self):
        return f'<Watchlist {self.id}: User {self.user_id} - Security {self.security_id}>'
