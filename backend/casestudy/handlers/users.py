from flask import request, jsonify

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
