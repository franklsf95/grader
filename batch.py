#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
import shutil
from batch.collect import collect
from batch.collect_votes import collect_votes
from batch.constants import *
from batch.late_chip import calc_late_days
from batch.generate_rubric import generate_rubric
from batch.grade import grade
from batch.make import make
from batch.pull import pull
from batch.push import push

DISPATCH = {
    'collect': collect,
    'collect-votes': collect_votes,
    'generate-rubric': generate_rubric,
    'grade': grade,
    'late-chip': calc_late_days,
    'make': make,
    'pull': pull,
    'push': push,
}


def main():
    parser = argparse.ArgumentParser(description='Batch operations for SVN repositories.')
    parser.add_argument('action', help='pull, grade or push')
    parser.add_argument('-f', '--force', help='grade, generate_rubric only. ignore existing grading',
                        action='store_true')
    parser.add_argument('-n', '--limit', help='for all. limit the number of repositories to process', type=int)
    parser.add_argument('-o', '--open', help='make only. open the Elm target after making', action='store_true')
    parser.add_argument('-r', '--repo', help='for all. run command on this specific repository')
    parser.add_argument('-s', '--skip', help='for all. skip the first SKIP repositories', type=int, default=0)
    args = parser.parse_args()

    # Dispatch function
    fn = DISPATCH.get(args.action, None)
    if fn is None:
        raise RuntimeError("> Don't know how to '{0}'".format(args.action))

    # If args.repo is set, run once and exit
    if args.repo is not None:
        fn(args.repo, Context(args, None, None))
        exit()

    # Read CSV for repositories
    summary = pd.read_csv(CLASS_SUMMARY)

    # Context can be modified
    ctx = Context(args, summary, ALIAS_POOL)
    return_values = []
    
    # Copy the solutions into elm-tester directory
    if args.action == 'grade':
        for solution in SOLUTION_FILES:
            shutil.copy(os.path.join(TESTS_DIR, HW_DIR,'solution', solution), os.path.join(ELM_TESTER_DIR, 'tests'))

    for i, repo in enumerate(summary['Repo']):
        if len(repo) == 0:
            continue
        if i < args.skip:
            print('> Skipping', repo)
            continue
        if type(args.limit) is int and i - args.skip >= args.limit:
            print('> Reached maximum number of repositories to process.')
            break
        if fn is not pull and not os.path.isdir(os.path.join(REPOS_DIR, repo, HW_DIR)):
            print("> Repository {0} does not have homework {1}, skipping".format(os.path.join(REPOS_DIR, repo, HW_DIR), HW_DIR))
            return_values.append(-1)
            continue

        ret = fn(repo, ctx)
        return_values.append(ret)

    print(return_values)

    if args.limit is not None or args.skip > 0:
        exit()

    # Further actions
    if args.action == 'grade':
        summary[HW_DIR] = return_values
        print(len(return_values))
        print(float(sum(return_values)) / len(return_values))
    elif args.action == 'late-chip':
        summary[HW_DIR + '_late_chip'] = return_values
    elif args.action == 'collect':
        summary[HW_DIR + '_alias'] = return_values

    # Write CSV
    summary.to_csv(CLASS_SUMMARY, index=False)

if __name__ == '__main__':
    main()
