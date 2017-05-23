#!/usr/bin/env python3

import math
from .constants import *

VOTING_FILE_PATH = os.path.join('voting', 'hw2-votes.txt')
ALT_VOTING_FILE_PATH = 'hw2-votes.txt'
VOTES_COLUMN = 'hw2_votes'


def __find_original(summary, alias):
    """
    Finds the original repository given an alias.
    :param summary: CSV
    :param alias: int
    :return: int, the index to the original repository
    """
    for idx, a in enumerate(summary['hw2_alias']):
        if not math.isnan(a) and int(a) == alias:  # an alias is an integer
            return idx
    return None


def collect_votes(repo_name, ctx):
    """
    Collect the votes from a repository and update the Context
    :param repo_name: string
    :param ctx: Context
    :return: none (side effect)
    """
    print('> Processing', repo_name, VOTES_COLUMN)
    repo_path = os.path.join(REPOS_DIR, repo_name)
    try:
        f = open(os.path.join(repo_path, VOTING_FILE_PATH))
    except FileNotFoundError:
        try:
            f = open(os.path.join(repo_path, ALT_VOTING_FILE_PATH))
        except FileNotFoundError:
            print('Voting file not found, skip')
            return
    vote_items = [line.rstrip() for line in f.readlines()]
    weight = 10
    for alias in vote_items:
        try:
            idx = __find_original(ctx.summary, int(alias))
        except ValueError:
            print('value error', alias)
            continue
        if idx is None:
            print('Error: invalid vote for', alias)
        else:
            if math.isnan(ctx.summary.get_value(idx, VOTES_COLUMN)):
                ctx.summary.set_value(idx, VOTES_COLUMN, 0)
            ctx.summary.set_value(idx, VOTES_COLUMN, ctx.summary.get_value(idx, VOTES_COLUMN) + weight)
        weight -= 1
        if weight == 0:
            break
