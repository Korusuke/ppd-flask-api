import os
import uuid
from flask import current_app, Blueprint, request, jsonify, make_response, send_file
from werkzeug.utils import secure_filename

files_bp = Blueprint('files_bp', __name__)


@files_bp.errorhandler(413)
def too_large(e):
    """
    Returns a 413 error if the uploaded 
    file is larger than 4096*4096
    """
    res = {
        'status': 'error',
        'message': 'File is too large'
    }
    return make_response(jsonify(res), 413)


@files_bp.route('/<string:project_name>')
def list_files(project_name):
    """
    Params:
        - project_name: project name created using /projects
    Returns:
        - input_file_paths: list of files present in the project folder 
    """
    if project_name == '':
        res = {
            'status': 'error',
            'message': 'Empty Project name'
        }
        return make_response(jsonify(res), 400)

    project_files = []
    project_name = secure_filename(project_name)
    project_folder = os.path.join(
        current_app.config['PROJECT_FILES_PATH'], project_name)

    if not os.path.isdir(project_folder):
        # error
        res = {
            'status': 'error',
            'message': 'Project does not exists',
            'project_name': project_name
        }
        return make_response(jsonify(res), 400)

    for path, subdirs, files in os.walk(project_folder):
        for name in files:
            project_files.append(name)
    res = {
        'total_files': len(project_files),
        'input_file_paths': project_files,
        'status': 'success'
    }
    return make_response(jsonify(res), 200)


@files_bp.route('/<string:project_name>', methods=['POST'])
def upload_file(project_name):
    """
    Path Param:
        - project_name: project name created using /projects
    Body Param:
        - File: the file to upload (must be of extension .pdb or .ppk)
    """
    uploaded_file = request.files['file']
    project_name = secure_filename(project_name)

    if project_name == '':
        res = {
            'status': 'error',
            'message': 'Invalid project name'
        }
        return make_response(jsonify(res), 400)

    project_folder = os.path.join(
        current_app.config['PROJECT_FILES_PATH'], project_name)

    if not os.path.isdir(project_folder):
        # error
        res = {
            'status': 'error',
            'message': 'Project does not exists',
            'project_name': project_name
        }
        return make_response(jsonify(res), 400)

    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            res = {
                'status': 'error',
                'message': 'Invalid file'
            }
            return make_response(jsonify(res), 400)

        file_path = os.path.join(project_folder, filename)
        uploaded_file.save(file_path)

        res = {
            'status': 'success',
            'message': 'File Created Succefully',
            'file_name': filename,
            'project_name': project_name
        }
        return make_response(jsonify(res), 200)

    res = {
        'status': 'error',
        'message': 'File Not Found'
    }
    return make_response(jsonify(res), 400)


@files_bp.route('/<string:projectname>/<string:filename>')
def download_file(projectname, filename):
    """
    Path Params:
        - project_name: project name created using /projects
        - filename: file name of the file inside the project that is to be downloaded
    Returns:
        - blob: the file to be downloaded as an attachment 
    """
    project_name = secure_filename(projectname)
    project_folder = os.path.join(
        current_app.config['PROJECT_FILES_PATH'], project_name)

    if not os.path.isdir(project_folder):
        # error
        res = {
            'status': 'error',
            'message': 'Project does not exists',
            'project_name': project_name
        }
        return make_response(jsonify(res), 400)

    filename = secure_filename(filename)

    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            res = {
                'status': 'error',
                'message': 'Invalid file requested'
            }
            return make_response(jsonify(res), 400)

        file_path = os.path.join(project_folder, filename)

        return send_file(file_path, as_attachment=True)

    res = {
        'status': 'error',
        'message': 'File Not Found'
    }
    return make_response(jsonify(res), 400)
