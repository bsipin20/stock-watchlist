import logging
from flask_cors import CORS
from flask import Flask
from redis import Redis

from celery.schedules import timedelta
from celery import Celery, Task

from casestudy import database
from casestudy.extensions import db, migrate, redis_client
from casestudy import config
from casestudy.seed import add_users
from casestudy.api import routes


def create_app(config_object=config.Config):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    for url in routes.ROUTES:
        app.add_url_rule(url, view_func=routes.ROUTES[url][0], methods=routes.ROUTES[url][1])    
    register_extensions(app)
    CORS(app, resources={r"*": {"origins": "http://localhost:3000"}})  # Allow only http://localhost:3000
    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    celery_init_app(app)
    app.cli.add_command(add_users)
    return None

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    celery_app.set_default()
    return celery_app

