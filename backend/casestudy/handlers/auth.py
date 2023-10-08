from flask import request, jsonify

user = {
        'username': 'user',
        'email': 'user@gmail.com',
        'first_name': 'John',
        'last_name': 'Doe',
}


def authenticate():
    query = request.args.get('username', '')  # Get the 'query' parameter from the URL
    return jsonify(user)
