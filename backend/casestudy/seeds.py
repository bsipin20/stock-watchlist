from random import uniform
from faker import Faker
from sqlalchemy import func
from .extensions import db
from .database import Security

fake = Faker()

def generate_fake_security_data(num_entries):
    """
    Generate fake security data.

    Parameters:
        num_entries (int): Number of fake entries to generate.

    Returns:
        list: List of dictionaries representing fake security data.
    """
    securities_data = []
    for _ in range(num_entries):
        ticker = fake.unique.word()[:4].upper()
        name = fake.company()
        description = fake.sentence()
        last_price = round(uniform(50.0, 2000.0), 2)
        securities_data.append({
            'ticker': ticker,
            'name': name,
            'description': description,
            'last_price': last_price
        })
    return securities_data

def seed_security_table(num_entries=10):
    """
    Seed the securities table with fake data.

    Parameters:
        num_entries (int): Number of fake entries to generate and insert.
    """
    securities_data = generate_fake_security_data(num_entries)
    for security_data in securities_data:
        security = Security(
            ticker=security_data['ticker'],
            name=security_data['name'],
            description=security_data['description'],
            last_price=security_data['last_price']
        )
        db.session.add(security)
    db.session.commit()

if __name__ == '__main__':
    # Seed the securities table with 10 fake entries
    seed_security_table(10)
    print('Security table seeded with fake data.')

