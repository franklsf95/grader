#!/usr/bin/env python3

from datetime import datetime
import math
import re
import subprocess
from .constants import *

DEADLINE = datetime.strptime('2017-04-10 12:00:00', '%Y-%m-%d %H:%M:%S')


def calc_late_days(repo_name, _):
    """
    Calculates the number of late chips used by one student for 1 assignment
    :param repo_name: string
    :param hw_num: int
    :return: int, number of late chips
    """
    oldest_datetime = datetime.utcfromtimestamp(0)
    for hw_file in HW_FILES:
        hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR, hw_file)

        # Extract the date time from each file in a homework repo and find the oldest time
        try:
            commit_info = str(subprocess.check_output(["svn", "info", hw_path]), 'utf-8')
            commit_datetime = get_commit_datetime(commit_info)
            if commit_datetime > oldest_datetime:
                oldest_datetime = commit_datetime

        except subprocess.CalledProcessError as e:
            print('FILE NOT FOUND ', repo_name, hw_file)

    late_chips = math.ceil((oldest_datetime - DEADLINE).total_seconds() / (24 * 60 * 60))
    return late_chips if late_chips > 0 else 0


def get_commit_datetime(commit_info):
    """
    Gets the datetime given a repo and a file
    :param commit_info: string
    :return: datetime obj, commited date
    """
    # Extract the date time and convert to a date time object
    commit_info = re.findall('Last Changed Date:(.*)', commit_info)[0].split(" ")[1:3]
    commit_datetime = datetime.strptime(commit_info[0] + " " + commit_info[1], "%Y-%m-%d %H:%M:%S")
    return commit_datetime
