class Config(object):
    """Base configuration."""
    MAX_CONTENT_LENGTH = 4096*4096
    UPLOAD_EXTENSIONS = ['.pdb', '.ppk']
    PROJECT_FILES_PATH = '/mnt/Vault/Projects/NYU/files'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'