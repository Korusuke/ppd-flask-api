from flask import Blueprint, jsonify, make_response
import json
from ppd.jobs.utils import test_task
from ppd import celery as celery_app
import redis
import itertools
from celery import states

redObj = redis.StrictRedis(host='localhost', port=6379, db=0)  # Queue

jobs_bp = Blueprint('jobs_bp', __name__)


@jobs_bp.route('/')
def get_running_jobs():
    # Get all pending tasks from redis
    pending_tasks = redObj.hgetall('unacked')
    # Get all tasks in celery
    x = celery_app.control.inspect()
    scheduled_tasks = [i for i in x.scheduled().values()]
    scheduled_tasks = list(itertools.chain(*scheduled_tasks))

    active_tasks = [i for i in x.active().values()]
    active_tasks = list(itertools.chain(*active_tasks))

    reserved_tasks = [i for i in x.reserved().values()]
    reserved_tasks = list(itertools.chain(*reserved_tasks))

    res = {
        'pending_tasks': {
            'total': len(pending_tasks),
            'task_ids': [json.loads(i.decode("utf-8"))[0]["headers"]["root_id"] for i in pending_tasks.values()]
        },
        'scheduled_tasks': {
            'total': len(scheduled_tasks),
            'task_ids': [i.get('id') for i in scheduled_tasks]
        },
        'active_tasks': {
            'total': len(active_tasks),
            'task_ids': [i.get('id') for i in active_tasks]
        },
        'reserved_tasks': {
            'total': len(reserved_tasks),
            'task_ids': [i.get('id') for i in reserved_tasks]
        }
    }
    return make_response(jsonify(res), 200)


@jobs_bp.route('/create', methods=['POST'])
def create_new_job():
    # TODO: Replace with rosetta
    a = test_task.delay(1, 2)
    b = test_task.delay(2, 3)
    c = test_task.delay(4, 5)
    r = [a.id, b.id, c.id]
    return str(r)


@jobs_bp.route('/status/<string:id>')
@jobs_bp.route('/result/<string:id>')
def job_status(id):
    print(id)
    task = test_task.AsyncResult(id)
    state = task.state
    res = {
        'task_id': id,
        'state': state
    }
    
    if state == states.SUCCESS:
        res['result'] = task.get()
    elif state == states.FAILURE:
        try:
            res['error'] = task.info.get('error')
        except Exception as e:
            res['error'] = 'Unknown error occurred'
    return make_response(jsonify(res), 200)
