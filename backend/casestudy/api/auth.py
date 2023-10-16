import logging
import sys

from flask import request, jsonify
from casestudy.extensions import db
from casestudy.database.models import User

def login():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return {'result': {'userId': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name}}, 200
    else:
        user = User(username=username, first_name="Albert", last_name="Employee")
        db.session.add(user)
        db.session.commit()
        return {'result': {'userId': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name}}, 200

