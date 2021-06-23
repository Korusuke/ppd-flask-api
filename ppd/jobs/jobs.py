from flask import Blueprint

jobs_bp = Blueprint('jobs_bp', __name__)


@jobs_bp.route('/')
def get_running_jobs():
    return 'Hello World'
