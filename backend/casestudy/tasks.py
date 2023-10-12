import os
import sys
import time
import logging
from flask import jsonify

import redis

from flask import current_app
from flask import Flask
from celery.schedules import timedelta
from celery import Celery
from celery.signals import after_setup_logger

from casestudy import database
from casestudy.app import celery_init_app, create_app
from casestudy.services.securities import update_security_prices, update_security_table

from casestudy.extensions import db, redis_client, socketio

app = create_app()

app.config.from_mapping(
    broker_url='redis://localhost:6379',
    result_backend='redis://localhost:6379',
    task_ignore_result=False,
)

celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, update_security_tickers.s('new'), name='add securities every 5')
    sender.add_periodic_task(5.0, create_task.s('hello'), name='add every 5')

@celery_app.task(name="create_task")
def create_task(arg):
    try:
        updated = update_security_prices()
        if updated:
            logging.info(f'Updated security prices')
        else:
            logging.error(f'Failed to update security prices')

    except Exception as e:
        logging.warning(f'Exception: {e}')
        raise e
        return False
    return True

@celery_app.task(name="update_security_tickers")
def update_security_tickers(arg):
    """
    Update the security tickers
    """
    updated = update_security_table()
    print('finished updating security tickers', file=sys.stderr)
    send_updated_data_to_room('room_name')
    if updated:
        logging.info(f'Updated security tickers')
        redis_client.get(f'websocket:security_tickers')
    else:
        logging.error(f'Failed to update security tickers')
    return True

def get_user_ids_in_room(room_name):
    redis_key = f'users_in_room:{room_name}'
    user_ids = redis_client.smembers(redis_key)
    return [int(user_id) for user_id in user_ids] if user_ids else []

@celery_app.task(name="sending user data")
def send_user_data(user_id):
    data = jsonify({'hey'})
    # Retrieve WebSocket connection ID from Redis
    socket_id = redis_client.get(f'websocket:{user_id}')
    if socket_id:
        logging.info(f'Sending user data to {user_id} on socket {socket_id.decode()}')
        socketio.emit('user_data', {'user_id': user_id, 'data': data}, room=socket_id.decode(), namespace='/user')

def get_user_ids_in_room(room_name):
    # Assuming you're storing user IDs in a Redis set named 'users_in_room:{room_name}'
    redis_key = f'users_in_room:{room_name}'
    user_ids = redis_client.smembers(redis_key)
    return [int(user_id) for user_id in user_ids] if user_ids else []
    
def send_updated_data_to_room(room_name):
    # Get a list of user_ids in the room (you'll need to implement this based on your application's logic)
    user_ids_in_room = get_user_ids_in_room(room_name)
    print(f'User ids in room: {user_ids_in_room}', file=sys.stderr)
    updated_data = 55555
    # Send updated data to each user in the room using Celery tasks
    for user_id in user_ids_in_room:
        send_user_data.apply_async(args=[user_id])

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.info(f'Customize Celery logger, default handler: {logger.handlers[0]}')

