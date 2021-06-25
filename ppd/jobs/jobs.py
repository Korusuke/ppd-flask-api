from flask import current_app, Blueprint, jsonify, make_response, request
import json
import os
import redis
import itertools
from ppd.jobs.utils import rosetta_task
from ppd import celery as celery_app
from celery import states
from werkzeug.utils import secure_filename

redObj = redis.StrictRedis(host='localhost', port=6379, db=0)  # Queue

jobs_bp = Blueprint('jobs_bp', __name__)


@jobs_bp.route('/')
def get_running_jobs():
    """
    Returns all jobs in queue, 
    including the ones in db but not in celery
    """
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
    """
    Start a new job with given flags
    Params:
        - flags - contents of flag file to be supplied to rosetta
        - project_name - Name of the project
    Returns:
        - task_id - celery task id for the new sim
    """
    # TODO: Replace with rosetta
    flags = request.form['flags']
    project_name = request.form['project_name']
    project_name = secure_filename(project_name)
    filename = f'flag_{project_name}'
    project_folder = os.path.join(
        current_app.config['PROJECT_FILES_PATH'], project_name)

    file_path = os.path.join(project_folder, filename)
    temp_file = os.path.join(project_folder, 'filename.temp')
    # save file
    print(flags)

    with open(temp_file, 'w') as f:
        f.writelines(flags)

    # Create actual file to remove CRLF
    with open(temp_file, "r") as inf:
        with open(file_path, "w") as fixed:
            for line in inf:
                fixed.write(line.rstrip() + '\n')
    os.remove(temp_file)

    task = rosetta_task.delay(project_name, flags)
    res = {
        'status': 'success',
        'message': 'sim started successfully',
        'task_id': task.id
    }
    return make_response(jsonify(res), 200)


@jobs_bp.route('/status/<string:id>')
@jobs_bp.route('/result/<string:id>')
def job_status(id):
    """
    Returns current status of the background celery task
    Params:
        - id - celery task id 
    Returns:
        - state - celery task state
        - result[Optional] - returns project name incase of success
        - error[Optional] - returns the traceback incase of failure 
    """
    print(id)
    task = rosetta_task.AsyncResult(id)
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
