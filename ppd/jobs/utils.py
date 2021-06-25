from ppd import celery as celery_app
import time
import os
import shlex
import subprocess
from flask import current_app


@celery_app.task(bind=True)
def rosetta_task(self, project_name, flags):
    project_folder = os.path.join(
        current_app.config['PROJECT_FILES_PATH'], project_name)

    log_file = os.path.join(project_folder, 'stdout')
    err_file = os.path.join(project_folder, 'stderr')

    base_cmd = 'python3 /mnt/Vault/Projects/NYU/test.py'
    flag_file = f' @flag_{project_name}'
    full_cmd = base_cmd + flag_file

    with open(log_file, "wb") as out, open(err_file, "wb") as err:
        process = subprocess.run(shlex.split(full_cmd),
                                 cwd=project_folder,
                                 stdout=out,
                                 stderr=err)

    return project_name
