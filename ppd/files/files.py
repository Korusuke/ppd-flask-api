import os
import uuid
from flask import current_app, Blueprint, request, jsonify, make_response
from werkzeug.utils import secure_filename

files_bp = Blueprint('files_bp', __name__)


@files_bp.errorhandler(413)
def too_large(e):
    res = {
        'status': 'error',
        'message': 'File is too large'
    }
    return make_response(jsonify(res), 413)


@files_bp.route('/')
def list_files():
    input_files = []
    for path, subdirs, files in os.walk(current_app.config['INPUT_FILES_PATH']):
        for name in files:
            input_files.append(os.path.join(path, name).lstrip(
                current_app.config['INPUT_FILES_PATH']))
    res = {
        'total_files': len(input_files),
        'input_file_paths': input_files,
        'status': 'success'
    }
    return make_response(jsonify(res), 200)


@files_bp.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            res = {
                'status': 'error',
                'message': 'Invalid file'
            }
            return make_response(jsonify(res), 400)
        # Generate Unique ID for the file and save
        id = str(uuid.uuid4())

        file_folder = os.path.join(current_app.config['INPUT_FILES_PATH'], id)
        os.makedirs(file_folder, exist_ok=True)

        file_path = os.path.join(file_folder, filename)
        uploaded_file.save(file_path)

        res = {
            'status': 'success',
            'message': 'File Created Succefully',
            'file_name': filename,
            'file_path': os.path.join(id, filename)
        }
        return make_response(jsonify(res), 200)

    res = {
        'status': 'error',
        'message': 'File Not Found'
    }
    return make_response(jsonify(res), 400)
