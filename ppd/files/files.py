import os
from flask import current_app, Blueprint, request
from werkzeug.utils import secure_filename

files_bp = Blueprint('files_bp', __name__)


@files_bp.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@files_bp.route('/')
def list_files():
    files = os.listdir(current_app.config['INPUT_FILES_PATH'])
    print(files)
    return str(files)


@files_bp.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    file_type = request.form['file_type']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return "Invalid file", 400
        uploaded_file.save(os.path.join(current_app.config['INPUT_FILES_PATH'], filename))
    return 'File Uploaded', 200
