from runpy import run_path

import pathlib

settings = run_path("deploy_config.py")
for project in settings['projects']:
    print('export TSPROJ="{}"'.format(pathlib.Path(project).absolute()))
