from ppd import celery as celery_app
import time

@celery_app.task(bind=True)
def test_task(self, arg1, arg2):
    # some long running task here
    print('111111')
    time.sleep(10)
    print('222222')
    print(arg1,arg2)
    return arg1+arg2