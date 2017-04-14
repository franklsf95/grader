#!/usr/bin/env python3

import subprocess
from .constants import *


def pull(repo_name, _):
    """
    Checks out or updates a repository.
    :param repo_name: string
    :param _: unused
    :return: None
    """
    repo_path = os.path.join(REPOS_DIR, repo_name)
    if os.path.exists(repo_path):
        print('> Updating', repo_name)
        subprocess.call(['svn', 'up'], cwd=repo_path)
    else:
        print('> Checking out', repo_name)
        repo_url = os.path.join(REPO_URL_PREFIX, repo_name)
        subprocess.call(['svn', 'co', repo_url], cwd=REPOS_DIR)
