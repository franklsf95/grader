#!/usr/bin/env python3

import subprocess
from .constants import *

REPO_URL_PREFIX = 'https://phoenixforge.cs.uchicago.edu/svn/'


def push(repo_name, _):
    """
    Push changes in a homework directory.
    :param repo_name: string
    :param _: unused
    :return: None
    """
    hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR)
    if not os.path.exists(hw_path):
        print('> Skipping', repo_name)
        return

    print('> Pushing', repo_name)
    subprocess.call(['svn', 'add', "{}.rubric.txt".format(HW_IDENTIFIER)], cwd=hw_path)
    subprocess.call(['svn', 'ci', '-m', '"Graded {}"'.format(HW_DIR)], cwd=hw_path)
