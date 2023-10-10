import os
import time
import logging

from celery.schedules import timedelta
from celery import Celery
from celery.signals import after_setup_logger
from casestudy import resource, database
from casestudy.app import celery_init_app, create_app
from casestudy.service.securities import update_security_prices, update_security_table
from flask import current_app
from flask import Flask

from casestudy.extensions import db

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
#    try:
    updated = update_security_table()
    if updated:
        logging.info(f'Updated security tickers')
    else:
        logging.error(f'Failed to update security tickers')
    return True

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.info(f'Customize Celery logger, default handler: {logger.handlers[0]}')


#celery.con

#celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
#celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
#application = current_app._get_current_object()

#celery.conf.beat_schedule = {
#    'periodic-task': {
#        'task': 'tasks.create_task.to_',
#        'schedule': timedelta(seconds=5),
#    },
#}

#celery.config['CELERYBEAT_SCHEDULE'] = {
#    # Executes every minute
#    'periodic_task-every-minute': {
#        'task': 'casestudy.tasks.create_task',
#        'schedule': timedelta(seconds=5)
#    }
#}

