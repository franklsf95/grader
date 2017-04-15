#!/usr/bin/env python3

import os

BASE_DIR = '/Users/kevinzen/Repos/Grading/'
HW_DIR = 'hw2'
HW_FILES = ['Pi.elm', 'pi.elm', 'ThumbPi.png', 'ThumbPi.jpg']
FILES_DIR = os.path.join(BASE_DIR, 'grader', 'files')
REPOS_DIR = os.path.join(BASE_DIR, 'repositories/')
TESTS_DIR = os.path.join(BASE_DIR, 'cs22300-sp17/tests/')
CLASS_SUMMARY = os.path.join(BASE_DIR, 'class_summary.csv')
MAX_SCORE = 80

"""
CLASS_SUMMARY file headers:
['Repo', 'Late_Chips_Left', 'hw1', 'hw2', 'hw3', 'hw4', ' hw5', 'hw6', 'hw7', 'midterm', 'final', 'project']
"""
