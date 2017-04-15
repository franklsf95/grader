#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from batch.make import make
from batch.grade import grade
from batch.late_chip import calc_late_days
from batch.pull import pull
from batch.constants import *

DISPATCH = {
    'grade': grade,
    'late-chip': calc_late_days,
    'make': make,
    'pull': pull,
    'push': None,
}


def main():
    parser = argparse.ArgumentParser(description='Batch operations for SVN repositories.')
    parser.add_argument('action', help='pull, grade or push')
    parser.add_argument('-f', '--force', help='grade only. ignore existing grading', action='store_true')
    parser.add_argument('-n', '--limit', help='for all. limit the number of repositories to process', type=int)
    parser.add_argument('-o', '--open', help='make only. open the Elm target after making', action='store_true')
    args = parser.parse_args()

    # Dispatch function
    fn = DISPATCH.get(args.action, None)
    if fn is None:
        raise RuntimeError("> Cannot perform action '{0}'".format(args.action))

    # Read CSV for repositories
    summary = pd.read_csv(CLASS_SUMMARY)

    return_values = []
    for i, repo in enumerate(summary['Repo']):
        if len(repo) == 0:
            continue
        if type(args.limit) is int and i >= args.limit:
            print('> Reached maximum number of repositories to process.')
            break
        ret = fn(repo, args)
        return_values.append(ret)

    # Further actions
    if args.action == 'grade':
        summary[HW_DIR] = return_values
        summary.to_csv(CLASS_SUMMARY, index=False)
        print(len(return_values))
        print(float(sum(return_values)) / len(return_values))

    if args.action == 'late':
        summary[HW_DIR + "_late_chip"] = return_values
        print('Late chips Used', return_values)
        summary.to_csv(CLASS_SUMMARY, index=False)

if __name__ == '__main__':
    main()
