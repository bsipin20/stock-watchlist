import logging

from casestudy.extensions import db
from casestudy.resource import TestAlbertStockClient
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
    # Get unique security_ids from watchlist and join to get security tickers
    query = db.session.query(Watchlist.security_id, Security.ticker).\
        join(Security, Watchlist.security_id == Security.id).distinct()

    # Get a list of unique tickers
    tickers = [ticker for security_id, ticker in query]

    # Fetch the latest prices for all tickers using a single API call
    # Replace API_ENDPOINT and API_KEY with your actual endpoint and API key
    response = TestAlbertStockClient("base_resource").get_stock_prices_by_tickers(tickers)
    logging.info(f'response: {response}')

    # Assuming the response contains prices in a dictionary with tickers as keys
    # Update the security price tracker table with the latest prices
    for security_id, ticker in query.all():
        last_price = response[ticker]
        security_price = SecurityPriceTracker(security_id=security_id, last_price=last_price)
        logging.info(f'security_price: {security_price}')
        db.session.add(security_price)

    # Commit the changes to the database
    db.session.commit()
    return True