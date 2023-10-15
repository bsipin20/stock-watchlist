import sys
from datetime import datetime, timezone
import pytz
import logging
from datetime import datetime

from flask import jsonify, make_response
from flask import current_app
from casestudy.database.dao import SecurityDao, WatchlistDao
from casestudy.resource import get_stock_client
from casestudy.extensions import db, redis_client

class SecurityService:
    def __init__(self, security_dao, watchlist_dao, stock_client):
        self.security_dao = security_dao
        self.watchlist_dao = watchlist_dao
        self.stock_client = stock_client

    def search_security(self, query):
        result = self.security_dao.find_matching_securities_by_query(query)
        if result:
            securities = [{'id': sec.id, 'ticker': sec.ticker, 'name': sec.name} for sec in result]
            print(securities, file=sys.stderr)
            return securities
        else:
            return []
    
    def update_security_table(self):
        logging.info('Updating security table')
        existing_securities = self.security_dao.get_security_id_ticker_lookup()
        stock_api_response = self.stock_client.get_all_stocks()
        new_securities = []
        for ticker, name in stock_api_response.items():
            if ticker not in existing_securities:
                security = {'ticker': ticker, 'name': name}
                new_securities.append(security)

        if len(new_securities) > 0:
            logging.info(f'adding {len(new_securities)}')
            result = self.security_dao.update_security_table(new_securities)
            if result:
                num_added = result['num_added']
                logging.info(f'A total of {num_added} new securities were added to the database.')
            else:
                logging.info('No new securities were added to the database.')
        logging.info('Security table updated successfully')
        return True
    
    def update_security_prices(self):
        securities = self.security_dao.get_all_securities()
        tickers = [sec['ticker'] for sec in securities]
        logging.info(f'TICKERS: {tickers}')
        # absent update time from client this is the best we can
        # do for when the price was last updated
        utc_timestamp = int(datetime.now(timezone.utc).timestamp())
        stock_api_response = self.stock_client.get_stock_prices_by_tickers(tickers)
        security_update_input = []
        for security in securities:
            update = {
                'last_price': stock_api_response[security['ticker']],
                'last_updated': utc_timestamp,
                'ticker': security['ticker'],
                'security_id': security['security_id'],
                'name': security['name']
            }
            security_update_input.append(update)
        result = self.security_dao.update_security_prices(security_update_input)
        if result:
            logging.info(f'Updated security prices')
            return True
        else:
            return False

def create_security_service():
    security_dao = SecurityDao(db, redis_client)
    watchlist_dao = WatchlistDao(db, redis_client)
    with current_app.app_context():
        stock_client = get_stock_client(
            current_app.config['STOCK_API_URI'],
            current_app.config['STOCK_API_KEY'],
            current_app.config['ENVIRONMENT']
        )
    return SecurityService(security_dao, watchlist_dao, stock_client)



