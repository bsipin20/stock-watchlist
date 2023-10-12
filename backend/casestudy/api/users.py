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
    # Use a SQL join to fetch ticker symbols for the specified user_id
    ticker_symbols = db.session.query(Security.ticker).join(Watchlist, Watchlist.security_id == Security.id).filter(Watchlist.user_id == userId).all()
    
    # Extract ticker symbols from the query result
    ticker_symbols = [f'stock_prices:{symbol}' for (symbol,) in ticker_symbols]
    stock_price_bytes = redis_client.mget(ticker_symbols)
    stock_prices = [{'ticker': symbol, 'price': float(price) if price else None} for symbol, price in zip(ticker_symbols, stock_price_bytes)]
    last_updated = redis_client.get(f'stock_prices:updated_at')
    result = { 'last_updated': last_updated, 'stock_prices': stock_prices }
    response = { 'success': True , 'result': result }
    return jsonify(response), 200


def post_users_watch_list(userId):
    """
    Post a new watchlist entry for a user

    parameters:
        userId (int): The user id
    """
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

