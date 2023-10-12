import logging
import sys

from flask import request, jsonify
from casestudy.extensions import db
from casestudy.database import User

user = {
        'username': 'user',
        'email': 'user@gmail.com',
        'first_name': 'John',
        'last_name': 'Doe',
}

def login():
    data = request.get_json()
    username = data.get('username')
    user = User.query.filter_by(username=username).first()
    response = jsonify({"result": { "userId": user.id, "username": user.username}, "success": True})

    return response, 200

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
