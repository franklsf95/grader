#!/usr/bin/env python3

import os
from datetime import datetime

BASE_DIR = '/Users/luans/cs22300/'
HW_DIR = 'hw1'
HW_FILES = ['FPWarmup.elm']
REPO_URL_PREFIX = 'https://phoenixforge.cs.uchicago.edu/svn/'
REPOS_LIST_FILE = os.path.join(BASE_DIR, 'repositories_list.txt')
REPOS_DIR = os.path.join(BASE_DIR, 'repositories/')
TESTS_DIR = os.path.join(BASE_DIR, 'cs22300-sp17/tests/')
DEADLINE = datetime.strptime('2017-04-03 12:00:00', '%Y-%m-%d %H:%M:%S')
CLASS_SUMMARY = os.path.join(BASE_DIR, 'class_summary.csv')

"""
CLASS_SUMMARY file headers:
['Repo', 'Late_Chips_Left', 'hw1', 'hw2', 'hw3', 'hw4', ' hw5', 'hw6', 'hw7', 'midterm', 'final', 'project']
"""
