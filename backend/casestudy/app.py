"""App module for the flask app."""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from casestudy import routes
#from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

def start_app():
    """ Create the flask app."""
    app = Flask(__name__, instance_relative_config=False)

    for url in routes.ROUTES:
        app.add_url_rule(url, view_func=routes.ROUTES[url][0], methods=routes.ROUTES[url][1])    
    return app

