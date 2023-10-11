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

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        # Hash the password before storing it
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Verify the hashed password
        return check_password_hash(self.password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        # Perform any username validation if needed
        # For example, ensure it's a valid format
        # You can customize this validation based on your requirements
        # This is a simple example, and you can expand on it
        # For now, we'll just check if the length is at least 3 characters
        if len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return username

class Security(db.Model):
    """Model for a security"""
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(64), unique=True)

class SecurityPriceTracker(db.Model):
    """Model for tracking the price of a security"""
    id = db.Column(db.Integer, primary_key=True)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'), nullable=False, unique=True)
    last_price = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Watchlist(db.Model):
    """Model for a watchlist entry"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'), nullable=False)

    def __repr__(self):
        return f'<Watchlist {self.id}: User {self.user_id} - Security {self.security_id}>'
