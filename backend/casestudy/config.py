import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class DevelopmentConfig():
    TESTING = False
    WTF_CSRF_ENABLED = False

class Config(object):
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_PORT = os.environ['DB_PORT']
    DB_NAME = os.environ['DB_NAME']
    REDIS_URL = os.environ['REDIS_URL']
    STOCK_API_CLIENT = os.environ['TEST_CLIENT']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@db:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND =  REDIS_URL
