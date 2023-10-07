from casestudy import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Security(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    last_price = db.Column(db.Float)

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'), nullable=False)

    def __repr__(self):
        return f'<Watchlist {self.id}: User {self.user_id} - Security {self.security_id}>'
