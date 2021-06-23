class Config(object):
    """Base configuration."""
    MAX_CONTENT_LENGTH = 4096*4096
    UPLOAD_EXTENSIONS = ['.pdb', '.ppk']
    INPUT_FILES_PATH = '/mnt/Vault/Projects/NYU/files/input_files'
    OUTPUT_FILES_PATH = '/mnt/Vault/Projects/NYU/files/output_files'
    LOG_FILES_PATH = '/mnt/Vault/Projects/NYU/files/log_files'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'