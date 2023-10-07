from datetime import datetime
from pytz import timezone
from flask import jsonify, request


utc_timezone = timezone('UTC')

securities = [
    {'ticker': 'AAPL', 'name': 'Apple Inc.'},
    {'ticker': 'MSFT', 'name': 'Microsoft Corporation'},
    {'ticker': 'TSLA', 'name': 'Tesla Inc.'},
    {'ticker': 'GOOG', 'name': 'Alphabet Inc.'},
    {'ticker': 'AMZN', 'name': 'Amazon.com Inc.'},
    {'ticker': 'FB', 'name': 'Facebook Inc.'},
    {'ticker': 'BRK.A', 'name': 'Berkshire Hathaway Inc.'}
]

user_data = [
    {  'id': 1, 

     'watch_list':  [
        { 
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'last_price': '127.35'
        },
        {
            'ticker': 'TSLA',
            'name': 'Tesla Inc.',
            'last_price': '609.89'
        },
        {
            'ticker': 'MSFT',
            'name': 'Microsoft Corporation',
            'last_price': '249.07'
        }
        ]
    },
    { 'id': 2,
     'watch_list':  [
        { 
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'last_price': '127.35'
        }
        ]
    }
]

def find_user_by_id(userId):
    for user in user_data:
        if user['id'] == userId:
            return user
    return None

def find_matching_securities(search):
    matches = []
    for security in securities:
        if search in security['ticker'].lower() or search in security['name'].lower():
            matches.append(security)
    return matches

def health():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

def get_users_watch_list(userId):
    resp = jsonify(succes=True)
    resp.status_code = 200
    response = find_user_by_id(userId)
    return jsonify(response)

def post_users_watch_list(userId, ticker):
    if request.method == 'POST':
        # return 404 if cant find user
        # return 204 if successful
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp
    elif request.method == 'DELETE':
        # RETURN 404 if cant find
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp
    else:
        "GOT HERE"
    return None

def get_securities():
    response = { 'last_updated': datetime.now(utc_timezone).isoformat(), 'securities': securities }
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

def authenticate(username, password):
    for user in user_data:
        if user['username'] == username and user['password'] == password:
            return user
    return None

ROUTES = {
    '/v1/health': (health, ['GET']),
    '/v1/users/<int:userId>/watch_list': (get_users_watch_list, ['GET']),
    '/v1/users/<int:userId>/watch_list/<string:ticker>': (post_users_watch_list, ['POST', 'DELETE']),
    '/v1/securities/search': (search_securities, ['GET']),
    '/v1/securities/': (get_securities, ['GET']),
    '/v1/auth/': (authenticate, ['POST'])
}
