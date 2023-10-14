import sys

from flask import request, jsonify

from sqlalchemy.orm import joinedload
from casestudy.extensions import db, redis_client
from casestudy.database import Watchlist, Security, SecurityPriceTracker

from casestudy.services import user_watchlist_service
from casestudy.services.user_watchlist_service import UserWatchListService

class UserRequest(BaseModel):
    userId: int

class WatchListItem(BaseModel):
    ticker: str
    name: str
    last_price: float
    last_updated: str

class WatchlistResponse(BaseModel):
    success: boolean
    error: Optional[str]
    data: Optional[WatchListItem]

def build_watch_list_response(watch_lists):
    response = WatchlistResponse(success=True, error=None, data=[])
    for watch_list in watch_lists:
        response.data.append(WatchListItem(watch_list))
    return response

def get_users_watch_list(userId):
    """
    Get the watchlist for a user
    parameters:
        userId (int): The user id
    """
    try:
        user_request = UserRequest(userId=userId)
        user_watch_list_service = create_user_watch_list_service()
        watch_list = user_watch_list_service.get_watchlist_by_user_id(user_request, db)
        response = build_watch_list_response(watch_list)
        return jsonify(response), 200
    except DatabaseConnectionError as e:
        response = {'success': False, 'error': 'The server is currently unable to handle the request. Please try again later.'}
        return jsonify(response), 500
    except RedisConnectionError as e:
        response = {'success': False, 'error': 'The server is currently unable to handle the request. Please try again later.'}
        return jsonify(response), 500
    except Exception as e:
        response = {'success': False, 'error': 'The server is currently unable to handle the request. Please try again later.'}
        return jsonify(response), 500


class WatchlistRequest(BaseModel):
    userId = int
    securityId = int

def post_add_users_watch_list(userId):
    """
    
    Post a new watchlist entry for a user

    parameters:
        userId (int): The user id
    """
    try:
        security_id = request.json.get('security_id')
        user_request = WatchlistRequest(userId=userId, securityId=securityId)
        user_watch_list_service = create_user_watch_list_service()
        result = user_watch_list_service.add_watchlist_entry(watch_list_request)
        if result:
            return jsonify({'message': 'Watchlist entry added successfully'}), 201
        else:
            return jsonify({'message': 'Watchlist entry already exists for this user and security'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid security_id'}), 400
    

#def post_remove_users_watch_list(userId):
#    try:
#        security_id = request.json.get('security_id')
#        user_request = WatchlistRequest(userId=userId, securityId=securityId)
#        user_watch_list_service = create_user_watch_list_service()
#        result = user_watch_list_service.remove_watchlist_entry(watchlist_request)
#    if not existing_watchlist_entry:
#        return jsonify({'message': 'Cannot '}), 200
#    else:
#        db.session.delete(existing_watchlist_entry)
#        db.session.commit()
#        return jsonify({'message': 'Watchlist entry deleted successfully'}), 200
