from flask import Blueprint

files_bp = Blueprint('files_bp', __name__)


@files_bp.route('/')
def list_files():
    return 'Hello Waorld'
