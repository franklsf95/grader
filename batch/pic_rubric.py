#!/usr/bin/env python3

from .constants import *
import pandas as pd
import math


REASON_HEADER = HW_DIR + "_reason"
GOOD_COMMENT = "Good Job "
NO_FILE = "Did not find your file"
def gen_pic_rubric(repo_name, _):
    """
    Pulls comments from respective column on class_summary
    And adds it to each repository as a file in the format of hw1.rubric.txt
    """
    hw_path = os.path.join(REPOS_DIR, repo_name, HW_DIR)
    rubric_filename = "{0}.rubric.txt".format(HW_DIR)
    rubric_path = os.path.join(hw_path, rubric_filename)
    summary = pd.read_csv(CLASS_SUMMARY)
    reason = list(summary[summary['Repo'] == repo_name][REASON_HEADER])[0]
    score = list(summary[summary['Repo'] == repo_name][HW_DIR])[0]

    if type(reason) != str and math.isnan(reason): # perfect score
        if score == 80:
            text = GOOD_COMMENT + __format_score(MAX_SCORE, MAX_SCORE)
        else:text = NO_FILE + __format_score(0, MAX_SCORE)

    else: text = reason + __format_score(score, MAX_SCORE)

    with open(rubric_path, 'w') as f:
        f.write(text)

def __format_score(score , max):
    return "\nScore : " + str(score) + "/" + str(max)
