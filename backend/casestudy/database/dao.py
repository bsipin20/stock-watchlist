"""
The goal was to separate database specific logic from the rest of the application logic
"""
import sys
import logging

from casestudy.database.models import Security, Watchlist

class WatchlistDao:
    def __init__(self, db, redis_client):
        """
        Initialize the WatchlistDao.

        Params:
        db: The database instance.
        redis_client: The Redis client for caching.
        """
        self.db = db
        self.redis_client = redis_client

    def get_ticker_symbols_by_user_id(self, user_id):
        """ gets ticker symbols by user id"""
        ticker_symbols = self.db.session.query(Security.ticker).join(Watchlist, Watchlist.security_id == Security.id).filter(Watchlist.user_id == user_id).all()
        return ticker_symbols

    def get_existing_watchlist_entry(self, user_id, security_id):
        """
        Get ticker symbols in a user's watchlist.

        Params:
        user_id (int): The unique identifier of the user.

        Return values:
        list: A list of ticker symbols.
        """
        result = self.db.session.query(Watchlist).filter_by(user_id=user_id, security_id=security_id).first()
        return result
    
    def get_existing_watchlist_securities(self):
        """ Get existing watchlist securities"""
        query = self.db.session.query(Watchlist.security_id, Security.ticker, Security.name).join(Security, Watchlist.security_id == Security.id).distinct()
        watchlist_items = []
        for row in query:
            watchlist_items.append({'security_id': row[0], 'ticker': row[1], 'name': row[2]})
        return watchlist_items
    
    def add_security_to_user_watchlist(self, user_id, security_id):
        """
        Adds a security to a user's watchlist.

        Params:
        user_id (int): The unique identifier of the user. id from User table
        security_id (int): The unique identifier of the security. id from Security table

        Return values:
        Watchlist: The new watchlist entry.
        """
        new_watchlist_entry = Watchlist(user_id=user_id, security_id=security_id)
        self.db.session.add(new_watchlist_entry)
        self.db.session.commit()
        return new_watchlist_entry

    def delete_ticker_from_user_watch_list(self, user_id, security_id):
        """
        Deletes a security from a user's watchlist.

        Params:
        user_id (int): The unique identifier of the user. id from User table
        security_id (int): The unique identifier of the security. id from Security table

        Return values:
        bool: True or false if a security was deleted from a user's watchlist.
        """
        existing_watch_list_entry = Watchlist.query.filter_by(user_id=user_id, security_id=security_id).first()
        if existing_watch_list_entry:
            self.db.session.delete(existing_watch_list_entry)
            self.db.session.commit()
            return True
        else:
            return False

class SecurityInsertException(Exception):
    pass

class SecurityDao:

    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client
    
    def get_security_id_ticker_lookup(self):
        """
        Gets all lookup of security IDs and corresponding tickers.

        Return values:
        dict: A dictionary where keys are security IDs and values are corresponding tickers.
        """
        existing_security_names = dict([(key, value) for key, value in self.db.session.query(Security.ticker, Security.name).all()])
        return existing_security_names

    def get_security_by_id(self, security_id):
        """
        Gets security information by ID.

        Params:
        security_id (int): The unique identifier of the security.

        Return values:
        dict: A dictionary containing security information.
        """
        security = self.db.session.query(Security).filter_by(id=security_id).first()
        result = { 'id': security.id, 'ticker': security.ticker, 'name': security.name }
        return result

    def update_security_table(self, securities):
        """
        Updates the security table with new securities.

        Params:
        securities (list): A list of dictionaries representing securities.

        Return values:
        dict: A dictionary containing the number of securities added.
        """
        num_added = 0
        for i in securities:
            new_security = Security(name=i['name'], ticker=i['ticker'])
            self.db.session.add(new_security)
            num_added += 1
        self.db.session.commit()
        return { 'num_added': num_added }

    def get_all_securities(self):
        """
        Gets all securities.

        Return values:
        list: A list of dictionaries containing security information.
        """
        query = self.db.session.query(Security.id, Security.ticker, Security.name).distinct()
        watchlist_items = []
        for row in query:
            watchlist_items.append({'security_id': row[0], 'ticker': row[1], 'name': row[2]})
        return watchlist_items

    def add_new_securities(self, securities):
        """ Adds new securities to the database
        Params:
        securities (list): A list of dictionaries representing securities.

        Return values:
        True if successful
        """
        try:
            for security in securities:
                new_security = Security(name=security['name'], ticker=security['ticker'])
                self.db.session.add(new_security)
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            raise SecurityInsertException(f"Error adding securities: {str(e)}")

    def find_matching_securities_by_query(self, query):
        """ finds matching securities by query

        Params:
        query (str): The search query.

        Return values:
        list: A list of dictionaries containing security information.
        """
        securities = self.db.session.query(Security).filter(
            (Security.name.ilike(f'%{query}%')) | (Security.ticker.ilike(f'%{query}%'))).all()
        return securities

    def update_security_prices(self, securities):
        """ finds security prices by ticker

        Params:
        securities (list): A list of dictionaries representing securities.

        Return values:
        True if cache was updated successfully
        """
        for security in securities:
            ticker = security['ticker']
            security_key = f'stock_info:{ticker}'.lower()
            self.redis_client.hmset(security_key, security)
        return True
    
    def get_latest_prices(self, securities):
        """ Gets latest prices for securities


        Params:
        securities (list): A list of dictionaries representing securities.


        Return values:
        list[dict]: A list of dictionaries containing security information.
        """
        keys = [f'stock_info:{ticker}'.lower() for (ticker, ) in securities]
        result = []
        for key in keys:
            latest_security_price_info = self.redis_client.hgetall(key)
            if latest_security_price_info:
                parsed_info = {key.decode('utf-8'): value.decode('utf-8') for key, value in latest_security_price_info.items()}
                result.append(parsed_info)
        return result
