import logging
from flask import current_app
from casestudy.extensions import db, redis_client
from casestudy.database.dao import WatchlistDao, SecurityDao
    
class WatchlistService:
    """ service for handling watchlist related operations"""


    def __init__(self, watchlist_dao, security_dao):
        """
        Initialize the WatchlistService.

        Parameters:
        watchlist_dao: Data access object for user watchlist-related data. see casestudy.database.dao.WatchlistDao
        security_dao: Data access object for security-related data. see casestudy.database.dao.SecurityDao
        """
        self.watchlist_dao = watchlist_dao
        self.security_dao = security_dao

    def get_security_prices_by_user_id(self, user_id):
        """
        Get security prices for securities in a user's watchlist.

        Parameters:
        user_id (int): The unique identifier of the user.

        Returns:
        dict: A dictionary containing security prices for the user's watchlist.
        False: If the watchlist is empty or an error occurs. If i had more time I would think more about return structs here


        """
        watch_list = self.watchlist_dao.get_ticker_symbols_by_user_id(user_id)
        if len(watch_list) > 0:
            response = self.security_dao.get_latest_prices(watch_list)
            return response
        else:
            False

    def add_security_to_watchlist(self, user_id, security_id):
        """
        Add a security to a user's watchlist.

        Parameters:
        user_id (int): The unique identifier of the user.
        security_id (int): The unique identifier of the security.

        Returns:
        bool: True if the security was added successfully, False if it already exists in the watchlist.
        """
        existing_watch_list_entry = self.watchlist_dao.get_existing_watchlist_entry(user_id, security_id)
        if existing_watch_list_entry:
            return False
        else:
            new_entry = self.watchlist_dao.add_security_to_user_watchlist(user_id, security_id)
            return new_entry
    
    def delete_security_from_watchlist(self, user_id, security_id):
        """
        Delete a security from a user's watchlist.

        Parameters:
        user_id (int): The unique identifier of the user.
        security_id (int): The unique identifier of the security.

        Returns:
        bool: True if the security was added. If had mor time would think about return structs here and exceptions
        """
        self.watchlist_dao.delete_ticker_from_user_watch_list(user_id, security_id)
        return True

def create_watchlist_service():
    """
    Create and configure a WatchlistService instance.

    Returns:
    WatchlistService: An instance of the WatchlistService.
    """
    watchlist_dao = WatchlistDao(db, redis_client)
    security_dao = SecurityDao(db, redis_client)
    service = WatchlistService(watchlist_dao, security_dao)
    return service