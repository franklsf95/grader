#!/usr/bin/env python3

import shutil
import subprocess
from .constants import *

ELM_PACKAGE_FILE = 'elm-package.json'
OUTPUT_FILE = 'Pi.html'


def make(repo_name, args):
    """
    Call elm-build each repository.
    :param repo_name: string
    :param args: dict
    :return: None
    """
    hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR)

    # Copy the elm-package.json file
    shutil.copy(os.path.join(FILES_DIR, ELM_PACKAGE_FILE), hw_path)

    # Make
    ret = subprocess.call(['elm-make', '--yes'] + HW_FILES + ['--output', OUTPUT_FILE], cwd=hw_path)

    # Open
    if ret == 0 and args.open:
        subprocess.call(['open', OUTPUT_FILE], cwd=hw_path)

    # Cleanup
    try:
        os.remove(os.path.join(hw_path, ELM_PACKAGE_FILE))
    except FileNotFoundError:
        pass
