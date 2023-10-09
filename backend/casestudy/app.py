import logging

from casestudy.extensions import db, migrate
from casestudy import routes, seeds, config
from flask_cors import CORS
from flask import Flask
from celery.schedules import timedelta
from celery import Celery, Task
from casestudy import resource, database
from casestudy.extensions import db

def create_app(config_object=config.Config):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    for url in routes.ROUTES:
        app.add_url_rule(url, view_func=routes.ROUTES[url][0], methods=routes.ROUTES[url][1])    
    register_extensions(app)
    CORS(app, resources={r'/*' : {'origins': "*"}}, supports_credentials=True)
    return app

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    #celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    return celery_app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    celery_init_app(app)
    return None
