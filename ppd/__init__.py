from celery import Celery
celery = Celery('ppd', config_source='ppd.celeryconfig')
