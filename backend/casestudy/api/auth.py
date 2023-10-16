import logging
import sys

from flask import request, jsonify
from casestudy.extensions import db
from casestudy.database.models  import User

def login():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    response = jsonify(
            {"result": {
                "userId": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username}, "success": True
             }
            )
    return response, 200

