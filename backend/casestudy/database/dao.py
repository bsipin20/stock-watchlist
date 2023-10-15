import sys
import logging

from casestudy.database.models import Security, Watchlist

class WatchlistDao:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client

    def get_ticker_symbols_by_user_id(self, user_id):
        ticker_symbols = self.db.session.query(Security.ticker).join(Watchlist, Watchlist.security_id == Security.id).filter(Watchlist.user_id == user_id).all()
        return ticker_symbols

    def get_existing_watchlist_entry(self, user_id, security_id):
        result = self.db.session.query(Watchlist).filter_by(user_id=user_id, security_id=security_id).first()
        return result
    
    def get_existing_watchlist_securities(self):
        query = self.db.session.query(Watchlist.security_id, Security.ticker, Security.name).join(Security, Watchlist.security_id == Security.id).distinct()
        watchlist_items = []
        for row in query:
            watchlist_items.append({'security_id': row[0], 'ticker': row[1], 'name': row[2]})
        return watchlist_items
    
    def add_security_to_user_watchlist(self, user_id, security_id):
        new_watchlist_entry = Watchlist(user_id=user_id, security_id=security_id)
        self.db.session.add(new_watchlist_entry)
        self.db.session.commit()
        return new_watchlist_entry

    def delete_ticker_from_user_watch_list(self, user_id, security_id):
        existing_watch_list_entry = Watchlist.query.filter_by(user_id=user_id, security_id=security_id).first()
        if existing_watch_list_entry:
            self.db.session.delete(existing_watch_list_entry)
            self.db.session.commit()
            return True
        else:
            return False

class SecurityDao:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client

    def get_security_id_ticker_lookup(self):
        existing_security_names = dict([(key, value) for key, value in self.db.session.query(Security.ticker, Security.name).all()])
        return existing_security_names

    def update_security_table(self, securities):
        num_added = 0
        for i in securities:
            new_security = Security(name=i['name'], ticker=i['ticker'])
            self.db.session.add(new_security)
            num_added += 1
        self.db.session.commit()
        return { 'num_added': num_added }

    def get_all_securities(self):
        query = self.db.session.query(Security.id, Security.ticker, Security.name).distinct()
        watchlist_items = []
        for row in query:
            watchlist_items.append({'security_id': row[0], 'ticker': row[1], 'name': row[2]})
        return watchlist_items
    def add_new_securities(self, securities):
        for security in securities:
            new_security = Security(name=security['name'], ticker=security['ticker'])
            self.db.session.add(new_security)
        self.db.session.commit()
        return True

    def find_matching_securities_by_query(self, query):
         securities = self.db.session.query(Security).filter(
            (Security.name.ilike(f'%{query}%')) | (Security.ticker.ilike(f'%{query}%'))).all()
         return securities

    def update_security_prices(self, securities):
        for security in securities:
            ticker = security['ticker']
            security_key = f'stock_info:{ticker}'.lower()
            self.redis_client.hmset(security_key, security)
        return True
    
    def get_latest_prices(self, securities):
        keys = [f'stock_info:{ticker}'.lower() for (ticker, ) in securities]
        result = []
        for key in keys:
            latest_security_price_info = self.redis_client.hgetall(key)
            if latest_security_price_info:
                parsed_info = {key.decode('utf-8'): value.decode('utf-8') for key, value in latest_security_price_info.items()}
                result.append(parsed_info)
        return result
    
