import logging
from datetime import datetime
from pytz import timezone
from flask import jsonify, request
from casestudy.database import Security
from casestudy.extensions import db

securities = [
    {'ticker': 'AAPL', 'name': 'Apple Inc.'},
    {'ticker': 'MSFT', 'name': 'Microsoft Corporation'},
    {'ticker': 'TSLA', 'name': 'Tesla Inc.'},
    {'ticker': 'GOOG', 'name': 'Alphabet Inc.'},
    {'ticker': 'AMZN', 'name': 'Amazon.com Inc.'},
    {'ticker': 'FB', 'name': 'Facebook Inc.'},
    {'ticker': 'BRK.A', 'name': 'Berkshire Hathaway Inc.'}
]

UTC_TIMEZONE = timezone('UTC')

def _find_matching_securities(search):
    matches = []
    for security in securities:
        if search.lower() in security['ticker'].lower() or search.lower() in security['name'].lower():
            matches.append(security)
    return matches

def get_securities():
    securities = Security.query.all()
    results = []
    for security in securities:
        logging.info(security)
        results.append({ 'ticker': security.ticker, 'name': security.name, 'id': security.id})
    return {'success': True, 'results': results}

def search_securities():
    query = request.args.get('query', '')  # Get the 'query' parameter from the URL
    if query == '':
        return jsonify([])
    else:
        result = _find_matching_securities(query)
        if result:
            #TODO replace with pydantic validator
            response = { 'results': { 'securities': result }, 'success': True }
            print(response)
            return jsonify(response)
        return jsonify([])