from flask import request, jsonify

from casestudy.extensions import db
from casestudy.database import Watchlist, Security

user_data = [
    {  'id': 1, 

     'watch_list':  [
        { 
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'last_price': '127.35'
        },
        {
            'ticker': 'TSLA',
            'name': 'Tesla Inc.',
            'last_price': '609.89'
        },
        {
            'ticker': 'MSFT',
            'name': 'Microsoft Corporation',
            'last_price': '249.07'
        }
        ]
    },
    { 'id': 2,
     'watch_list':  [
        { 
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'last_price': '127.35'
        }
        ]
    }
]

def find_user_by_id(userId):
    for user in user_data:
        if user['id'] == userId:
            return user
    return None

def get_users_watch_list(userId):
    resp = jsonify(success=True)
    resp.status_code = 200
    response = find_user_by_id(userId)
    return jsonify(response)

def post_users_watch_list(userId):
    try:
        request_json = request.get_json()
        security_id = int(request_json['security_id'])
    except ValueError:
        return jsonify({'error': 'Invalid security_id'}), 400

    # Validate security exists before adding to watchlist
    if not Security.query.filter_by(id=security_id).first():
        return jsonify({'error': 'Invalid security_id - Security not found'}), 400

    # Check if the user_id and security_id combination already exists in the watchlist
    existing_watchlist_entry = Watchlist.query.filter_by(user_id=userId, security_id=security_id).first()

    if existing_watchlist_entry:
        return jsonify({'message': 'Watchlist entry already exists for this user and security'}), 200

    # Create a new watchlist entry
    new_watchlist_entry = Watchlist(user_id=userId, security_id=security_id)

    try:
        db.session.add(new_watchlist_entry)
        db.session.commit()
        return jsonify({'message': 'Watchlist entry added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
