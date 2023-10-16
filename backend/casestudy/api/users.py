"""
Module: users.py

This module contains functions and data structures related to managing a user's watchlist for securities.
It defines API endpoints for retrieving, adding, and deleting securities from the user's watchlist.

Functions:
    - get_user_watch_list(userId): Retrieve the watchlist for a user.
    - post_security_to_user_watchlist(userId): Add a new security to the user's watchlist.
    - delete_security_user_watchlist(userId, securityId): Delete a security from the user's watchlist.
"""
from typing import Optional, List
from dataclasses import dataclass

from flask import Flask, request, jsonify

from casestudy.extensions import db, redis_client
from casestudy.services.watchlist_service import create_watchlist_service
from casestudy.services.security_service import create_security_service


@dataclass
class SecurityPrices:
    """
    Represents security prices information.

    Attributes:
    ticker (str): The ticker symbol of the security.
    name (str): The name of the security.
    last_price (str): The last price of the security (as a string, as per client's expectation).
    last_updated (int): The last update timestamp in UTC.
    security_id (str): The unique identifier for the security (as a string, as per client's expectation).
    """
    ticker: str
    name: str
    last_price: str # client expects a string
    last_updated: int # utc timestamp
    security_id: str # client expects string

@dataclass
class UserWatchlistResponse:
    """
    Represents the response for a user's watchlist.

    Attributes:
    success (bool): Indicates if the operation was successful.
    results (Optional[List[SecurityPrices]]): List of security prices objects in the user's watchlist.
    message (str): A message providing additional information.
    """
    success: bool
    results: Optional[List[SecurityPrices]]
    message: str

def get_user_watch_list(userId):
    """
    Route Handler: Get User Watchlist

    This route handler retrieves the watchlist for a specific user.

    Parameters:
    userId (int): The unique identifier of the user.

    Returns:
    JSON response: A JSON response containing the user's watchlist.

    Example Response:
    {
        "success": true,
        "results": [
            {
                "ticker": "AAPL",
                "name": "Apple Inc.",
                "last_price": "135.45",
                "last_updated": 1634302542,
                "security_id": "12345"
            },
            {
                "ticker": "GOOGL",
                "name": "Alphabet Inc.",
                "last_price": "2725.36",
                "last_updated": 1634302541,
                "security_id": "67890"
            }
        ],
        "message": ""
    }
    """
    watchlist_service = create_watchlist_service()
    users_watchlist = watchlist_service.get_security_prices_by_user_id(userId)
    if users_watchlist:
        result_list = []
        for i in users_watchlist:
            prices = SecurityPrices(
                ticker=i['ticker'],
                name=i['name'],
                last_price=str(i['last_price']),
                last_updated=i['last_updated'],
                security_id=str(i['security_id'])
            )
            result_list.append(prices)
        response = UserWatchlistResponse(success=True, results=result_list, message='')
        return jsonify(response), 200
    else:
        response = {'success': False , 'message': 'No watchlist items found', 'data': []}
        return jsonify(response), 200

def post_security_to_user_watchlist(userId):
    """
    Route Handler: Add Security to User Watchlist

    This route handler adds a new security to a user's watchlist.

    Parameters:
    userId (int): The unique identifier of the user.

    Request Body:
    {
        "security_id": "<security_id>"
    }

    Returns:
    JSON response: A JSON response indicating the success of the operation.

    Example Response (Success):
    {
        "success": true,
        "message": "Security added to watchlist successfully"
    }

    Example Response (Failure - Security already exists in watchlist):
    {
        "success": false,
        "message": "Security already exists in watchlist"
    }
    """
    obj = request.get_json()
    security_id = obj.get('security_id')
    watchlist_service = create_watchlist_service()
    result = watchlist_service.add_security_to_watchlist(userId, security_id)
    if result:
        # if added to watchlist, update the cache with the latest price
        security_service = create_security_service()
        security_service.get_latest_security_price(security_id)
        response = { 'success': True , 'message': 'Security added to watchlist successfully'}
        return jsonify(response), 200
    else:
        response = { 'success': False , 'message': 'Security already exists in watchlist'}
        return jsonify(response), 200

def delete_security_user_watchlist(userId, securityId):
    """
    Route Handler: Delete Security from User Watchlist

    This route handler deletes a security from a user's watchlist.

    Parameters:
    userId (int): The unique identifier of the user.
    securityId (int): The unique identifier of the security to be deleted from the watchlist.

    Returns:
    JSON response: A JSON response indicating the success of the operation.

    Example Response (Success):
    {
        "success": true,
        "message": "Security deleted from watchlist successfully"
    }
    """
    watchlist_service = create_watchlist_service()
    result = watchlist_service.delete_security_from_watchlist(userId, securityId)
    response = { 'success': True , 'message': 'Security deleted from watchlist successfully'}
    return response, 200