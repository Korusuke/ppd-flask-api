import os
import uuid
from flask import current_app, Blueprint, request, jsonify, make_response
from werkzeug.utils import secure_filename

projects_bp = Blueprint('projects_bp', __name__)


@projects_bp.route('/')
def list_projects():
    """Returns a list of all project folders"""
    projects = [f.name for f in os.scandir(
        current_app.config['PROJECT_FILES_PATH']) if f.is_dir()]

    res = {
        'total_projects': len(projects),
        'project_names': projects,
        'status': 'success'
    }
    return make_response(jsonify(res), 200)


@projects_bp.route('/', methods=['POST'])
def create_new_project():
    """Creates a new project folder"""
    project_name = request.form['project_name']
    print(project_name)

    foldername = secure_filename(project_name)
    if foldername == '':
        res = {
            'status': 'error',
            'message': 'Invalid folder name',
            'project_name': foldername
        }
        return make_response(jsonify(res), 400)

    project_folder = os.path.join(
        current_app.config['PROJECT_FILES_PATH'], foldername)

    if os.path.isdir(project_folder):
        # error
        res = {
            'status': 'error',
            'message': 'Project Already exists',
            'project_name': foldername
        }
        return make_response(jsonify(res), 400)
    else:
        # create and success

        os.makedirs(project_folder, exist_ok=True)

        res = {
            'status': 'success',
            'message': 'Project Created Succefully',
            'project_name': foldername
        }
        return make_response(jsonify(res), 200)

    res = {
        'status': 'error',
        'message': 'Unknown error occured'
    }
    return make_response(jsonify(res), 400)
