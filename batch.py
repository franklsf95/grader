#!/usr/bin/env python3

import argparse
import os
import subprocess

REPO_URL_PREFIX = 'https://phoenixforge.cs.uchicago.edu/svn/'
REPOS_LIST_FILE = '../repositories_list.txt'
REPOS_DIR = '../repositories/'


def pull(repo_name):
    """
    Checkout or update a SVN repository.
    :param repo_name: string
    """
    repo_path = os.path.join(REPOS_DIR, repo_name)
    if os.path.exists(repo_path):
        print('Updating', repo_name)
        subprocess.call(['svn', 'up'], cwd=repo_path)
    else:
        print('Checking out', repo_name)
        repo_url = os.path.join(REPO_URL_PREFIX, repo_name)
        subprocess.call(['svn', 'co', repo_url], cwd=REPOS_DIR)


def main():
    parser = argparse.ArgumentParser(description='Batch operations for SVN repositories.')
    parser.add_argument('action', help='pull, grade or push')
    args = parser.parse_args()

    # Dispatch function
    fn = {
        'pull': pull
    }[args.action]
    if fn is None:
        raise RuntimeError('Cannot perform action ' + args.action)

    # Get the list of repositories
    with open(REPOS_LIST_FILE) as f:
        repos = [line.strip() for line in f.readlines()]

    # Perform action on each repository
    for repo in repos:
        fn(repo)

if __name__ == '__main__':
    main()
