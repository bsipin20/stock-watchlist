from casestudy.extensions import db, redis_client
from casestudy.database.dao import WatchlistDao, SecurityDao
    
class WatchlistService:
    def __init__(self, watchlist_dao, security_dao):
        self.watchlist_dao = watchlist_dao
        self.security_dao = security_dao

    def get_security_prices_by_user_id(self, user_id):
        watch_list = self.watchlist_dao.get_ticker_symbols_by_user_id(user_id)
        if watch_list:
            response = self.security_dao.get_latest_prices(watch_list)
            return response
        else:
            False

    def add_security_to_watchlist(self, user_id, security_id):
        existing_watch_list_entry = self.watchlist_dao.get_existing_watchlist_entry(user_id, security_id)
        if existing_watch_list_entry:
            return False
        else:
            new_entry = self.watchlist_dao.add_security_to_user_watchlist(user_id, security_id)
            #TODO
            return new_entry
    
    def delete_security_from_watchlist(self, user_id, security_id):
        self.watchlist_dao.delete_ticker_from_user_watch_list(user_id, security_id)

def create_watchlist_service():
    watchlist_dao = WatchlistDao(db, redis_client)
    security_dao = SecurityDao(db, redis_client)
    service = WatchlistService(watchlist_dao, security_dao)
    return service