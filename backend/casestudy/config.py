import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_PORT = '5432'
DB_NAME = 'postgres'

class DevelopmentConfig():
    TESTING = False
    WTF_CSRF_ENABLED = False

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@db:{DB_PORT}/{DB_NAME}'
   # SQLALCHEMY_DATABASE_URI = f'postgresql://user:password@localhost:{DB_PORT}/database1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
