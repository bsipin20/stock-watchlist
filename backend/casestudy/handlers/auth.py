user_data = [ {'id': 1, 'username': 'user1', 'password': 'user2'} ]

def authenticate(username, password):
    for user in user_data:
        if user['username'] == username and user['password'] == password:
            return user
    return None
