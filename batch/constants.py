#!/usr/bin/env python3

import os
from .context import Context

BASE_DIR = '/Users/kevinzen/Repos/Grading'
HW_DIR = 'hw3'
HW_IDENTIFIER = HW_DIR.replace('/', '.')
HW_FILES = ['ListsAndTrees.elm']
FILES_DIR = os.path.join(BASE_DIR, 'grader', 'files')
REPOS_DIR = os.path.join(BASE_DIR, 'repositories/')
TESTS_DIR = os.path.join(BASE_DIR, 'cs22300-sp17/tests/')
CLASS_SUMMARY = os.path.join(BASE_DIR, 'cs223-spr-17-admin', 'class_summary.csv')
ALIAS_POOL = ['10301', '10501', '10601', '11311', '11411', '12421', '12721', '12821', '13331', '13831', '13931', '14341', '14741', '15451', '15551', '16061', '16361', '16561', '16661', '17471', '17971', '18181', '18481', '19391', '19891', '19991', '30103', '30203', '30403', '30703', '30803', '31013', '31513', '32323', '32423', '33533', '34543', '34843', '35053', '35153', '35353', '35753', '36263', '36563', '37273', '37573', '38083', '38183', '38783', '39293', '70207', '70507', '70607', '71317', '71917', '72227', '72727', '73037', '73237', '73637', '74047', '74747', '75557', '76367', '76667', '77377', '77477', '77977', '78487', '78787', '78887', '79397', '79697', '79997', '90709', '91019', '93139', '93239', '93739', '94049', '94349', '94649', '94849', '94949', '95959', '96269', '96469', '96769', '97379', '97579', '97879', '98389', '98689']

"""
Origin of alias pool: https://oeis.org/A002385

CLASS_SUMMARY file headers:
['Repo', 'Late_Chips_Left', 'hw1', 'hw2', 'hw3', 'hw4', ' hw5', 'hw6', 'hw7', 'midterm', 'final', 'project']
"""
