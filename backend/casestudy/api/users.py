from flask import request, jsonify

from sqlalchemy.orm import joinedload
from casestudy.extensions import db
from casestudy.database import Watchlist, Security, SecurityPriceTracker

def get_users_watch_list(userId):
    """
    Get the watchlist for a user
    parameters:
        userId (int): The user id
    """
    user_watchlist = db.session.query(Watchlist).filter_by(user_id=userId).all()
    watchlist_info = []

    # Iterate through the watchlist and get the associated security details
    for watchlist_item in user_watchlist:
        security_id = watchlist_item.security_id

        # Retrieve the security details (ticker, name) and latest price
        security_details = db.session.query(Security, SecurityPriceTracker.last_price).\
            join(SecurityPriceTracker, SecurityPriceTracker.security_id == security_id).\
            filter(Security.id == security_id).first()

        if security_details:
            security = security_details[0]
            security_ticker = security.ticker
            security_name = security.name
            last_price = security_details[1]

            # Append the information to the results list
            watchlist_info.append({
                "security_id": security_id,
                "security_ticker": security_ticker,
                "security_name": security_name,
                "last_price": last_price
            })
    return jsonify(watchlist_info)

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
