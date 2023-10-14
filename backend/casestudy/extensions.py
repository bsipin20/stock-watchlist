from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
import redis

db = SQLAlchemy()
migrate = Migrate()
redis_client = redis.Redis(host='redis', port=6379, db=0)

def get_or_create_db_session():
    global db

    if db.session:
        return db.session
    else:
        db.init_app