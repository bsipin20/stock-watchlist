"""App module for the flask app."""
from flask import Flask, request, jsonify
from casestudy import routes

def start_app():
    """ Create the flask app."""
    app = Flask(__name__, instance_relative_config=False)
    for url in routes.ROUTES:
        app.add_url_rule(url, view_func=routes.ROUTES[url][0], methods=routes.ROUTES[url][1])    
    return app
