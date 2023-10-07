from datetime import datetime
from pytz import timezone
from flask import jsonify, request

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

def find_matching_securities(search):
    matches = []
    for security in securities:
        if search in security['ticker'].lower() or search in security['name'].lower():
            matches.append(security)
    return matches


def get_securities():
    response = { 'last_updated': datetime.now(UTC_TIMEZONE).isoformat(), 'securities': securities }
    return jsonify(response)

def search_securities():
    query = request.args.get('query', '')  # Get the 'query' parameter from the URL
    if query == '':
        print("NOTHING HERE")
    else:
        result = find_matching_securities(query)
        if result:
            return jsonify(result)
        return jsonify([])
