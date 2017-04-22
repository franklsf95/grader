#!/usr/bin/env python3

from collections import namedtuple
import os

BASE_DIR = '/Users/luans/cs22300/'
HW_DIR = 'hw2'
HW_FILES = ['Pi.elm']
FILES_DIR = os.path.join(BASE_DIR, 'grader', 'files')
REPOS_DIR = os.path.join(BASE_DIR, 'repositories/')
TESTS_DIR = os.path.join(BASE_DIR, 'cs22300-sp17/tests/')
CLASS_SUMMARY = os.path.join(BASE_DIR, 'class_summary.csv')

Context = namedtuple('Context', ['args', 'summary'])

"""
CLASS_SUMMARY file headers:
['Repo', 'Late_Chips_Left', 'hw1', 'hw2', 'hw3', 'hw4', ' hw5', 'hw6', 'hw7', 'midterm', 'final', 'project']
"""
