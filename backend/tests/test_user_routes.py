import os
import pytest
import subprocess
from dotenv import load_dotenv

from casestudy.app import create_app
from casestudy.config import Config
from casestudy.extensions import db
from flask_migrate import Migrate
from casestudy.database.models import User, Security

class IntegrationTestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

class IntegrityError(Exception):
    pass

def seed_database():
    try:
        user1 = User(username='user1', first_name='John', last_name='Doe')
        user2 = User(username='user2', first_name='Jane', last_name='Doe')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    # Seed Security table
    securities_data = [
        {'ticker': 'AAPL', 'name': 'Apple Inc.'},
        {'ticker': 'GOOGL', 'name': 'Alphabet Inc.'}
    ]
    for security_data in securities_data:
        security = Security(**security_data)
        db.session.add(security)
    db.session.commit()

@pytest.fixture
def app():

    load_dotenv()
    app = create_app(IntegrationTestConfig)

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
        subprocess.run(["flask", "db", "upgrade"])

    with app.app_context():
        seed_database()

    yield app

     # Teardown: Drop all tables and remove the database
    with app.app_context():
        db.session.remove()
        db.drop_all()
#        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')

@pytest.fixture
def client(app):
    return app.test_client()

def test_search_endpoint(client):
    sample_response_data = { 
        'results': [
                {
                    'id': 1,
                    'name': 'Apple Inc.',
                    'ticker': 'AAPL'
                }
            ],
        'success': True,
        'error': None
    }

    response = client.get('/v1/securities/search?query=appl')
    assert response.status_code == 200
    assert response.json == sample_response_data

def test_search_endpoint_invalid_query(client):
    response = client.get('/v1/securities/search?query=a')
    assert response.status_code == 422
    assert response.json == {'error': 'Query must be at least 3 characters long'}

def test_integration(client):
    response = client.post('/v1/login/', json={'username': 'user1', 'password': 'password'})
    user_id = response.json['result']['userId']

    # check watch list is blank
    #blank_response = client.get(f'/v1/users/{user_id}/watch_list')
    #blank_response.json == {'success': True, 'data': [], 'message': 'No watchlist items found'}
    #blank_response.status_code == 200

    # search for security
    search_response = client.get('/v1/securities/search?query=appl')
    search_response.json['results'][0]['ticker'] == 'AAPL'
    security_id = search_response.json['results'][0]['id']

    # add security to watch list
    client.post(f'/v1/users/{user_id}/watch_list/', json={'security_id': security_id})

    # check its not occupied
    #response = client.get(f'/v1/users/{user_id}/watch_list')
    #assert response.status_code == 200
    #assert response.status_code == 200
    #assert response.json == sample_response_data
