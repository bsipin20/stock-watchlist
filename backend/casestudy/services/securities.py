import logging
import sys
import pytz
from datetime import datetime

from casestudy.extensions import db, redis_client
from casestudy.services.resource import TestAlbertStockClient
from casestudy.database import Security, Watchlist, SecurityPriceTracker

def update_security_table():
    logging.info('Updating security table')
    response = TestAlbertStockClient("base_resource").get_all_stocks()
    existing_security_names = dict([(key, value) for key, value in db.session.query(Security.ticker, Security.name).all()])
    new_securities = []
    logging.info(f'response: {response}')

    for ticker, name in response.items():
        logging.info(f'ticker: {ticker}, name: {name}')
        if ticker not in existing_security_names:
            new_securities.append(Security(ticker=ticker, name=name))
        
    if new_securities:
        db.session.add_all(new_securities)
        db.session.commit()
        logging.info(f'A total of {len(new_securities)} new securities were added to the database.')
    
    logging.info('Security table updated successfully')
    return True

def update_security_prices():
    """
    Method to update security prices.
    """
    # Fetch all securities and create a dictionary with security IDs as keys
    securities = {security.id: security for security in db.session.query(Security).all()}
    
    # Get unique security_ids from watchlist and join to get security tickers
    query = db.session.query(Watchlist.security_id, Security.ticker).\
        join(Security, Watchlist.security_id == Security.id).distinct()

    security_dicts = [{'security_id': row.security_id, 'ticker': row.ticker, 'last_updated': str(datetime.now(pytz.utc))}
                      for row in query]

    # Get a list of unique tickers
    tickers_request = []
    for row in query:
        tickers_request.append(row.ticker)

    # Fetch the latest prices for all tickers using a single API call
    # Replace API_ENDPOINT and API_KEY with your actual endpoint and API key
    response = TestAlbertStockClient("base_resource").get_stock_prices_by_tickers(tickers_request)
    #prefixed_stock_prices = {f'stock_prices:{symbol}': price for symbol, price in response.items()}
    # Store the dictionaries in Redis

    for security_dict in security_dicts:
        security_dict['last_price'] = response[security_dict['ticker']]
        print(security_dict, file=sys.stderr)
        redis_key = f'stock_info:{security_dict["ticker"]}'
        print(redis_key.rstrip().lower(), file=sys.stderr)
        redis_client.hmset(redis_key.rstrip().lower(), security_dict)
    return True
