#!/usr/bin/env python3

from .constants import *
import math


REASON_HEADER = HW_DIR + "_reason"
GOOD_COMMENT = 'Good Job!'
NO_FILE_COMMENT = 'I did not find your file.'
HW_FULL_SCORE = 10


def generate_rubric(repo_name, ctx):
    """
    Pulls comments from respective column on class_summary
    And adds it to each repository as a file in the format of hw1.rubric.txt
    """
    hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR)
    rubric_filename = "{0}.rubric.txt".format(HW_IDENTIFIER)
    rubric_path = os.path.join(hw_path, rubric_filename)
    summary = ctx.summary
    reason = list(summary[summary['Repo'] == repo_name][REASON_HEADER])[0]
    score = list(summary[summary['Repo'] == repo_name][HW_DIR])[0]

    if type(reason) != str and math.isnan(reason):
        # perfect score
        if score == HW_FULL_SCORE:
            comment = GOOD_COMMENT
        else:
            comment = NO_FILE_COMMENT
    else:
        comment = reason

    text = __format_score(score, HW_FULL_SCORE) + comment + '\n'

    with open(rubric_path, 'w') as f:
        f.write(text)


def __format_score(score, full_score):
    return "Project Planning Total Score: {} / {}\n\nComment: ".format(int(score), full_score)
