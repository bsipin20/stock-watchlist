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
from casestudy.services.security_service import create_security_service

from casestudy.extensions import db, redis_client

app = create_app()

app.config.from_mapping(
    broker_url='redis://localhost:6379',
    result_backend='redis://localhost:6379',
    task_ignore_result=False,
)

celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(2000, update_security_tickers.s('new'), name='add securities every 5')
    sender.add_periodic_task(5.0, update_security_prices.s('hello'), name='add every 5')

@celery_app.task(name="create_task")
def update_security_prices(arg):
    try:
        security_service = create_security_service()
        updated = security_service.update_security_prices()
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
    security_service = create_security_service()
    updated = security_service.update_security_table()
    print('finished updating security tickers', file=sys.stderr)
    if updated:
        logging.info(f'Updated security tickers')
    else:
        logging.error(f'Failed to update security tickers')
    return True

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.info(f'Customize Celery logger, default handler: {logger.handlers[0]}')

