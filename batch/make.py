#!/usr/bin/env python3

import shutil
import subprocess
from .constants import *

ELM_PACKAGE_FILE = 'elm-package.json'
ELM_STUFF_DIR = 'elm-stuff'
OUTPUT_FILE = 'Pi.html'


def make(repo_name, ctx):
    """
    Call elm-build each repository.
    :param repo_name: string
    :param ctx: Context
    :return: None
    """
    print('> Making', repo_name)
    hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR)

    # Copy the elm-package.json file
    shutil.copy(os.path.join(FILES_DIR, ELM_PACKAGE_FILE), hw_path)

    # Make
    ret = subprocess.call(['elm-make', '--yes'] + HW_FILES + ['--output', OUTPUT_FILE], cwd=hw_path)

    # Open
    if ret == 0 and ctx.args.open:
        subprocess.call(['open', OUTPUT_FILE], cwd=hw_path)

    # Cleanup
    try:
        os.remove(os.path.join(hw_path, ELM_PACKAGE_FILE))
        shutil.rmtree(os.path.join(hw_path, ELM_STUFF_DIR))
    except FileNotFoundError:
        pass
