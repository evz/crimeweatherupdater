from raven import Client
from raven.contrib.celery import register_signal
import os
import pymongo
from datetime import datetime, timedelta
from celery import Celery
from loader import get_crimes, get_most_wanted
from dumper import dumpit, dump_by_temp, dump_to_csv

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

client = Client(os.environ['SENTRY_URL'])
register_signal(client)

@celery.task
def load():
    crimes = get_crimes()
    get_most_wanted()
    return crimes

@celery.task
def dump_json():
    c = pymongo.MongoClient()
    db = c['chicago']
    db.authenticate(os.environ['CHICAGO_MONGO_USER'], password=os.environ['CHICAGO_MONGO_PW'])
    crime = db['crime']
    weather = db['weather']
    start_date = datetime.now() - timedelta(days=14)
    end_date = datetime.now()
    dumpit(crime, weather, start_date=start_date, end_date=end_date)
    dump_by_temp(crime, weather)
    return 'Dumped. Dumped real good'

@celery.task
def dump_csv():
    c = pymongo.MongoClient()
    db = c['chicago']
    db.authenticate(os.environ['CHICAGO_MONGO_USER'], password=os.environ['CHICAGO_MONGO_PW'])
    crime = db['crime']
    weather = db['weather']
    csv_start = datetime.now().replace(month=1).replace(day=1).strftime('%Y-%m-%d')
    end = datetime.now() - timedelta(days=7)
    csv_end = end.strftime('%Y-%m-%d')
    csv_name = end.strftime('%Y')
    dump_to_csv(csv_start, csv_end, csv_name)
    return 'Dumped that CSV'
