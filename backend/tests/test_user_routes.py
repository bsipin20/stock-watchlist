import os
import pytest
from dotenv import load_dotenv
import subprocess

from casestudy.app import create_app
from casestudy.config import Config
from casestudy.extensions import db
from flask_migrate import Migrate
from casestudy.database.models import User, Security

class IntegrationTestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    USE_MOCK_STOCK_API_CLIENT = True

class IntegrityError(Exception):
    pass

def seed_database():
    try:
        user1 = User(username='user1', password='password1')
        user2 = User(username='user2', password='password2')
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
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')

@pytest.fixture
def client(app):
    return app.test_client()

def test_integration(client):
    sample_response_data = { 
        'results': {
            'securities': [
                {
                    'id': 1,
                    'name': 'Apple Inc.',
                    'ticker': 'AAPL'
                }
            ]
        },
        'success': True
    }

    response = client.get('/v1/securities/search?query=appl')
    assert response.status_code == 200
    assert response.json == sample_response_data
