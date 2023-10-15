"""
Module: watchlist_controller.py

This module contains functions and data structures related to managing a user's watchlist for securities.
It defines API endpoints for retrieving, adding, and deleting securities from the user's watchlist.

Functions:
    - get_user_watch_list(userId): Retrieve the watchlist for a user.
    - post_security_to_user_watchlist(userId): Add a new security to the user's watchlist.
    - delete_security_user_watchlist(userId, securityId): Delete a security from the user's watchlist.
"""
from dataclasses import dataclass

from flask import Flask, request, jsonify

from casestudy.extensions import db, redis_client
from casestudy.services.watchlist_service import create_watchlist_service

def get_user_watch_list(userId):
    """
    Get the watchlist for a user
    parameters:
        userId (int): The user id
    """
    watchlist_service = create_watchlist_service()
    users_watchlist = watchlist_service.get_security_prices_by_user_id(userId)
    if users_watchlist:
        response = { 'success': True , 'results': users_watchlist}
        return jsonify(response), 200
    else:
        response = { 'success': False , 'message': 'No watchlist items found', 'data': []}
        return jsonify(response), 200
@dataclass
class WatchlistRequest:
    userId: int
    securityId: int

def post_security_to_user_watchlist(userId):
    """
    
    Post a new watchlist entry for a user

    parameters:
        userId (int): The user id
    """
    obj = request.get_json()
    security_id = obj.get('security_id')
    watchlist_service = create_watchlist_service()
    result = watchlist_service.add_security_to_watchlist(userId, security_id)
    if result:
        response = { 'success': True , 'message': 'Security added to watchlist successfully'}
        return jsonify(response), 200
    else:
        response = { 'success': False , 'message': 'Security already exists in watchlist'}
        return jsonify(response), 200

def delete_security_user_watchlist(userId, securityId):
    watchlist_service = create_watchlist_service()
    result = watchlist_service.delete_security_from_watchlist(userId, securityId)
    response = { 'success': True , 'message': 'Security deleted from watchlist successfully'}
    return response, 200