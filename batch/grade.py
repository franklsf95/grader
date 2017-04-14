#!/usr/bin/env python3

import shutil
import grader
from .constants import *


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
