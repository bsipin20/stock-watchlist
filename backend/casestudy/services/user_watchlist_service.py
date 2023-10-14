import logging

from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from pydantic import Optional, List

from casestudy.extensions import db, redis_client
from casestudy.database.dao import SecurityPrices

class SecurityDao:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client

    def find_matching_security(self, query):
        securities = self.db.session.query(Security).filter(
            (Security.name.ilike(f'%{query}%')) | (Security.ticker.ilike(f'%{query}%'))).all()
        return securities

class WatchlistDao:
    def __init__(self, db):
        self.db = db

    def get_ticker_symbols_by_user_id(self, user_id):
        ticker_symbols = self.db.session.query(Security.ticker).join(Watchlist, Watchlist.security_id == Security.id).filter(Watchlist.user_id == userId).all()
        return ticker_symbols

    def add_ticker_to_user_watchlist(self, user_id, security_id):
        existing_watch_list_entry = self.db.session(Watchlist).query.filter_by(user_id=user_id, security_id=security_id).first()
        return existing_watch_list_entry
    
    def delete_ticker_from_user_watch_list(self, user_id, security_id):
        existing_watch_list_entry = Watchlist.query.filter_by(user_id=user_id, security_id=security_id).first()
        if existing_watch_list_entry:
            self.db.session.delete(existing_watch_list_entry)
            self.db.session.commit()
            return True
        else:
            return False

class BaseSecurityDao(abcs.ABC):
    @abcs.abstractmethod
    def get_security_by_id(self, security_id):
        raise NotImplementedError
    
    @abcs.abstractmethod
    def get_security_by_ticker(self, ticker):
        raise NotImplementedError

class SecurityDao:
    def __init__(self, redis_client, db):
        self.redis_client = redis_client
        self.db = db

    def get_security_price_info_by_id(self, security_id):
        security = db.session.query(Security).filter_by(id=securityId).first()
        security_dict = redis_client.hgetall(f'stock_info:{str(security.ticker).lower()}')
        decoded_data = {key.decode(): value.decode() for key, value in security_dict.items()}
        return decoded_data
 
    def get_latest_security_prices(self, ticker_symbols):
        keys = [f'stock_info:{ticker}'.lower() for (ticker, ) in ticker_symbols]
        response = []
        for redis_key in keys:
            security_dict = self.redis_client.hgetall(redis_key)
            if security_dict:
                security_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in security_dict.items()}
                response.append(security_dict)
        return response

class SecuritiesService:
    def __init__(self, security_price_dao):
        self.security_price_dao = security_price_dao

    def get_security_price_info_by_id(self, security_id):
        security = self.security_price_dao.get_security_by_id(security_id)
        if security:
            security_prices = self.security_price_dao.get_latest_security_prices(security.id)
            return security_prices
        else:
            False
        
    def search_securities(self, query):
        securities = self.security_price_dao.find_matching_security(query)
        if securities:
            response = self.security_price_dao.get_latest_security_prices(securities)
            return response
        else:
            False

class UserWatchListService:
    def __init__(self, watchlist_dao, security_price_dao, security_dao):
        self.watchlist_dao = watchlist_dao
        self.security_price_dao = security_price_dao
        self.security_dao = security_dao

    def get_ticker_symbols_by_user_id(self, user_id, db):
        watch_list = self.watchlist_dao.get_ticker_symbols_by_user_id(user_id, db)
        if watch_list:
            response = self.security_price_dao.get_latest_ticker_prices(watch_list, redis_client)
            return response
        else:
            False
    
    def add_security_from_watchlist(self, user_id, security_id):
        existing_watch_list_entry = self.watchlist_dao.add_ticker_to_user_watchlist(user_id, security_id)
        if existing_watch_list_entry:
            return False
        else:
            return True
    
    def remove_security_from_watchlist(self, user_id, security_id):
    

class DatabaseConnectionError(Exception):
    pass

class RedisConnectionError(Exception):
    pass

def create_user_watch_list_service():
    try:
        db_session = get_or_create_db_session()
    except Exception as e:
        logging.error(f'Error creating db session: {e}')
        raise DatabaseConnectionError(e)
    try:
        redis_instance = get_or_create_redis_client()
    except Exception as e:
        logging.error(f'Error creating redis instance: {e}')
        raise RedisConnectionError(e)

    watch_list_dao = WatchlistDao(db_session)
    security_price_dao = SecurityPricePrices(redis_instance, db_session)
    security_dao = SecurityDao(redis_instance, db_session)

    return UserWatchListService(watch_list_dao, security_price_dao, security_dao)
