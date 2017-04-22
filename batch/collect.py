#!/usr/bin/env python3

from glob import glob
import random
import shutil
from .constants import *

REQUIRED_FILES = ['Pi.html', 'ThumbPi.*']
DESTINATION_PATH = os.path.join(BASE_DIR, 'submissions')


def collect(repo_name, ctx):
    """
    Collect OUTPUT_FILE from a repository and assign an alias to it
    :param repo_name: string
    :param ctx: Context
    :return: string, the assigned alias
    """
    idx = random.randint(0, len(ctx.alias_pool) - 1)
    alias = ctx.alias_pool.pop(idx)
    print('> Collecting', repo_name, "(alias: {})".format(alias))
    hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR)
    dest_path = os.path.join(DESTINATION_PATH, alias)
    if os.path.exists(dest_path):
        print('> Warning: ', dest_path, 'already exists. Abort.')
        return alias
    else:
        os.makedirs(dest_path)

    # Copy the required files
    for regex in REQUIRED_FILES:
        for file in glob(os.path.join(hw_path, regex)):
            shutil.copy(file, dest_path)

    return alias
