import sys

from flask import request, jsonify

from sqlalchemy.orm import joinedload
from casestudy.extensions import db, redis_client
from casestudy.database import Watchlist, Security, SecurityPriceTracker

def get_users_watch_list(userId):
    """
    Get the watchlist for a user
    parameters:
        userId (int): The user id
    """
    ticker_symbols = db.session.query(Security.ticker).join(Watchlist, Watchlist.security_id == Security.id).filter(Watchlist.user_id == userId).all()
    keys = [f'stock_info:{ticker}'.lower() for (ticker, ) in ticker_symbols]
    response = []
    for redis_key in keys:
        security_dict = redis_client.hgetall(redis_key)
        if security_dict:
            security_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in security_dict.items()}
            response.append(security_dict)
    response = { 'success': True , 'data': response}
    return jsonify(response), 200

def post_users_watch_list(userId):
    """
    
    Post a new watchlist entry for a user

    parameters:
        userId (int): The user id
    """
    try:
        security_id = request.json.get('security_id')
    except ValueError:
        return jsonify({'error': 'Invalid security_id'}), 400
    
    if request.method == 'POST':
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
    else:
        if not Security.query.filter_by(id=security_id).first():
            return jsonify({'error': 'Invalid security_id - Security not found'}), 400

        existing_watchlist_entry = Watchlist.query.filter_by(user_id=userId, security_id=security_id).first()

        if not existing_watchlist_entry:
            return jsonify({'message': 'Cannot '}), 200
        else:
            db.session.delete(existing_watchlist_entry)
            db.session.commit()
            return jsonify({'message': 'Watchlist entry deleted successfully'}), 200
