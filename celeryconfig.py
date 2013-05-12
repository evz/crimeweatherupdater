import os
from celery.schedules import crontab

BROKER_URL = 'sqs://%s:%s@' % (os.environ['AWS_ACCESS_KEY'], os.environ['AWS_SECRET_KEY'])

CELERY_IMPORTS = ("tasks", )
CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "chicago",
    "taskmeta_collection": "celery_results",
    "user": os.environ['UPDATE_MONGO_USER'],
    "password": os.environ['UPDATE_MONGO_PW'],
}
CELERY_DEFAULT_QUEUE = 'crimevsweather'
CELERY_LOG_FILE=os.path.join(os.path.dirname(__file__), '../../run/celery.log')

CELERYBEAT_SCHEDULE = {
    'load-every-morning': {
        'task': 'tasks.load',
        'schedule': crontab(hour=5, minute=30),
     },
    'dump-every-morning': {
        'task': 'tasks.dump',
        'schedule': crontab(hour=5, minute=30),
     },
}