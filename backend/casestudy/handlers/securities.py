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
    securities = db.session.query(Security.name).distinct().all()
    unique_securities = [security[0] for security in securities]
    response_object = { 'results': unique_securities, 'success': True}
    return jsonify(response_object)

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
