from ppd.app import create_app
from ppd.config import Config
from ppd.celery_util import init_celery
from ppd import celery

app = create_app(Config)
init_celery(app, celery)
