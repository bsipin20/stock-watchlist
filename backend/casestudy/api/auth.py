import logging
import sys

from flask import request, jsonify
from casestudy.extensions import db
from casestudy.database.models import User

def login():
    """
    this is a basic hacky auth, the majority of the focus was on the app logic
    the user can create the user by passing in a username
    """
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return {'result': {'userId': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name}}, 200
    else:
        user = User(username=username, first_name="John", last_name="Smith")
        db.session.add(user)
        db.session.commit()
        return {'result': {'userId': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name}}, 200

