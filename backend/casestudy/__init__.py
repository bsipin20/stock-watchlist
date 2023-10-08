from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from casestudy import config, routes

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
migrate.init_app(app, db)

for url in routes.ROUTES:
    app.add_url_rule(url, view_func=routes.ROUTES[url][0], methods=routes.ROUTES[url][1])    

CORS(app, resources={r'/*' : {'origins': "*"}}, supports_credentials=True)
from casestudy import models
