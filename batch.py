#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess

import grader

HW_DIR = 'hw1'
HW_FILES = ['FPWarmup.elm']
REPO_URL_PREFIX = 'https://phoenixforge.cs.uchicago.edu/svn/'
REPOS_LIST_FILE = '../repositories_list.txt'
REPOS_DIR = '../repositories/'
TESTS_DIR = '../tests/'


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
        os.remove(os.path.join(tests_path, file))
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
        'pull': pull,
        'grade': grade,
    }.get(args.action, None)
    if fn is None:
        raise RuntimeError("Cannot perform action '{0}'".format(args.action))

    # Get the list of repositories
    with open(REPOS_LIST_FILE) as f:
        repos = [line.strip() for line in f.readlines()]

    # Perform action on each repository
    return_values = []
    for repo in repos:
        if len(repo) == 0:
            continue
        ret = fn(repo, args)
        return_values.append(ret)

    # Further actions
    if args.action == 'grade':
        print(len(return_values))
        print(float(sum(return_values)) / len(return_values))

if __name__ == '__main__':
    main()
