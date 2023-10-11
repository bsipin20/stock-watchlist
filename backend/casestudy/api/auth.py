import logging
import sys

from flask import request, jsonify
from casestudy.extensions import db
from casestudy.database import User

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

user = {
        'username': 'user',
        'email': 'user@gmail.com',
        'first_name': 'John',
        'last_name': 'Doe',
}

@jwt_required(locations=['headers'])
def test_protected_route():
    return jsonify({'msg': 'You are authorized to view this page!'})        

def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 401
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity=user.id)
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    try:
        # Create a new User instance
        new_user = User(username=username, password=password)
        logging.info(new_user)
        # Validate the User instance (this will trigger the @validates decorator in the User model)
        # This will raise a ValueError if the validation fails
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=user)
        response = jsonify({"message": "User registered successfully"})
        set_access_cookies(response, access_token)
        return response
    except ValueError as e:
        raise e
        # Handle validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        raise e
        # Handle other exceptions
        return jsonify({"error": str(e)}), 500
 


    return jsonify({"msg": "register successful"})