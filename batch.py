#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import math
from datetime import datetime
import grader
import pandas as pd
import re

BASE_DIR        = '/Users/kevinzen/Repos/Grading/'
HW_DIR          = 'hw1'
HW_FILES        = ['FPWarmup.elm']
REPO_URL_PREFIX = 'https://phoenixforge.cs.uchicago.edu/svn/'
REPOS_LIST_FILE = os.path.join(BASE_DIR, 'repositories_list.txt')
REPOS_DIR       = os.path.join(BASE_DIR,'repositories/')
TESTS_DIR       = os.path.join(BASE_DIR,'cs22300-sp17/tests/')
DEADLINE        = datetime.strptime("2017-04-03 12:00:00", "%Y-%m-%d %H:%M:%S")
CLASS_SUMMARY   = os.path.join(BASE_DIR, 'class_summary.csv')

# The structure of this file is a CSV with the following column headers
#['Repo', ' Late_Chips_Left', ' hw1', ' hw2', ' hw3', ' hw4'
#        ,' hw5', ' hw6', ' hw7', ' midterm', ' final', ' project']

def pull(repo_name,_):
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


def __report_zero(rubric_path, reason):
    """
    Creates a zero-score report for a repository.
    :param rubric_path: string
    :param reason: string
    :return: None
    """
    text = 'Total Score: 0\n\nReason: ' + reason
    with open(rubric_path, 'w') as f:
        f.write(text)

def calc_late_days(repo_name,_):
    """
    Calculates the number of late chips used by one student for 1 assignment
    :param repo_name: string
    :param hw_num: int
    :return: int, number of late chips
    """
    oldest_datetime = datetime.utcfromtimestamp(0)
    for hw_file in HW_FILES:
        hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR, hw_file)

        # Extract the date time from each file in a hw repo and find the oldest time
        try:
            commit_info     = str(subprocess.check_output(["svn", "info", hw_path]),'utf-8')
        
            commit_datetime = get_commit_datetime(commit_info)
            
            if commit_datetime > oldest_datetime:
                oldest_datetime = commit_datetime
                
        except subprocess.CalledProcessError as e:
            print("FILE NOT FOUND ", repo_name, hw_file)
            
        
    late_chips = math.ceil((oldest_datetime - DEADLINE).total_seconds()/(24*60*60))
    return late_chips if late_chips > 0 else 0

    

def get_commit_datetime(commit_info):
    """
    Gets the datetime given a repo and a file
    :param commit_info: string
    :return: datetime obj, commited date
    """
    # Extract the date time and convert to a date time object
    commit_info         = re.findall('Last Changed Date:(.*)', commit_info)[0].split(" ")[1:3]
    commit_datetime     = datetime.strptime(commit_info[0] + " " + commit_info[1], "%Y-%m-%d %H:%M:%S")
    return commit_datetime


#def update_summary_late_chip():
#    """
#    Generates data table which summarizes each student's grades and 
#    number of late chips used.
#    :return: nothing
#    """
#    print("Updating All Late Chips ...\n")
#    summary = pd.read_csv(CLASS_SUMMARY)
#    summary['Late_Chips_Left'] -= summary['Repo'].apply(calc_late_days)
#    summary.to_csv(CLASS_SUMMARY, index = False)

def grade(repo_name, args):
    """
    Grades a repository for a homework by calling the grader module.
    :param repo_name: string
    :param args: arguments for grading
    :return: int, the grade
    """
    return_score = 0
    print('> Grading', repo_name, HW_DIR)
    hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR)
    tests_path = os.path.join(TESTS_DIR, HW_DIR)
    rubric_filename = "{0}.rubric.txt".format(HW_DIR)
    rubric_path = os.path.join(hw_path, rubric_filename)
    try:
        # Skip if graded
        if not args.force and os.path.exists(rubric_path):
            print('> Skip, graded')
            return
        # Make sure the homework directory exists
        if not os.path.exists(hw_path):
            os.makedirs(hw_path)
        # Delete existing report file
        os.remove(rubric_path)
        # Copy files into the testing directory
        for file in HW_FILES:
            shutil.copy(os.path.join(hw_path, file), tests_path)
        # Run grader
        argv = ['-v', tests_path, '-o', rubric_path]
        if len(HW_FILES) > 0:
            argv.append('-d')
            argv.extend(HW_FILES)
        return_score = grader.grade(argv)
    except FileNotFoundError as e:
        __report_zero(rubric_path, "I cannot find the required file {0}.".format(e.filename))
    except grader.TestingFailureError as e:
        __report_zero(rubric_path, "Automated testing crashed.")

    # Cleanup
    try:
        for file in HW_FILES:
            os.remove(os.path.join(tests_path, file))
    except FileNotFoundError:
        pass
    return return_score


def main():
    parser = argparse.ArgumentParser(description='Batch operations for SVN repositories.')
    parser.add_argument('action', help='pull, grade or push')
    parser.add_argument('-f', '--force', help='ignore existing grading', action='store_true')
    args = parser.parse_args()

    # Dispatch function
    fn = {
        'pull' : pull,
        'grade': grade,
        'late' : calc_late_days,
    }.get(args.action, None)
    if fn is None:
        raise RuntimeError("Cannot perform action '{0}'".format(args.action))

    summary = pd.read_csv(CLASS_SUMMARY)

    # Get the list of repositories
#    with open(REPOS_LIST_FILE) as f:
#        repos = [line.strip() for line in f.readlines()]
#
#    # Perform action on each repository
    return_values = []
    for repo in summary["Repo"]:
        if len(repo) == 0:
            continue
        ret = fn(repo, args)
        return_values.append(ret)
#    return_values = summary['Repo'].apply(fn, args)
    

    # Further actions
    if args.action == 'grade':
        summary[HW_DIR] = return_values
        summary.to_csv(CLASS_SUMMARY, index = False)
        print(len(return_values))
        print(float(sum(return_values)) / len(return_values))
        
    if args.action == 'late':
        summary[HW_DIR+"_late_chip"] = return_values
        print("Late chips Used", return_values)
        summary.to_csv(CLASS_SUMMARY, index =  False)


if __name__ == '__main__':
    main()
