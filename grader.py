#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import yaml

ELM_TESTER_DIR = './elm-tester'
TEMPLATE_FILENAME = 'report_template.txt'
TESTS_FILENAME = 'Tests.elm'
RUBRIC_FILENAME = 'rubric.yaml'


def decode_rubric(rubric_file):
    """
    Parses the rubric file (YAML) into a Python object.
    :param rubric_file: string
    :return: a dictionary
    """
    with open(rubric_file) as f:
        rubric = yaml.load(f)
    return rubric


def decode_result(result_raw):
    """
    Parses the testing result into a Python object.
    :param result_raw: bytes, raw output from Elm
    :return: a list of dictionaries
    """
    result_str = result_raw.stdout.decode('utf-8')
    lines = result_str.split('\n')
    result = []
    for line in lines:
        if len(line) > 0:
            result.append(json.loads(line))
    return result


def get_status(test_result, test, test_suite):
    """
    Gets the test result for a particular test in a particular test suite.
    :param test_result: string
    :param test: string
    :param test_suite: string
    :return: boolean
    """
    for item in test_result:
        labels = item['labels']
        if len(labels) < 2:
            raise RuntimeError('Bad test label: ' + labels)
        suite = labels[-2]
        name = labels[-1]
        if suite == str(test_suite) and name == str(test):
            test_result.remove(item)
            if item['status'] == 'pass':
                return True
            elif item['status'] == 'fail':
                return False
            else:
                raise RuntimeError('Bad test result: ' + item['status'])
    raise RuntimeError("Cannot find test result for {0} {1}".format(test_suite, test))


def generate_report(test_result, rubric):
    """
    Generates a test report based on test result and rubric.
    :param test_result: test result
    :param rubric: rubric
    :return: string
    """
    test_result = list(filter(lambda e: e['event'] == 'testCompleted', test_result))
    # Initialization
    report = []
    total = 0
    my_total = 0
    # Iterate over tests
    for test_suite in rubric:
        subtotal = 0
        my_subtotal = 0
        tests = rubric[test_suite]
        report.append("Test Suite: {0}".format(test_suite))
        report.append('')
        for item in tests:
            test, score = item.popitem()
            status = get_status(test_result, test, test_suite)
            my_score = score if status else 0
            subtotal += score
            my_subtotal += my_score
            report.append("  - Test Case {0}: {1} / {2}".format(test, my_score, score))
        report.append('')
        report.append("  Subtotal: {0} / {1}".format(my_subtotal, subtotal))
        report.append('')
        total += subtotal
        my_total += my_subtotal
    # Format result
    report = ["Total Score: {0} / {1}".format(my_total, total), ''] + report
    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(description='Set up and run Elm automated testing.')
    parser.add_argument('test_dir', help='directory containing test files and rubric')
    parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        print('Preparing to run test suite ' + args.test_dir + "...")
    shutil.copyfile(os.path.join(args.test_dir, TESTS_FILENAME), os.path.join(ELM_TESTER_DIR, 'tests', TESTS_FILENAME))

    if args.verbose:
        print('Running tests... ', end='')
    result_raw = subprocess.run(['elm-test', '--report', 'json'], cwd=ELM_TESTER_DIR, stdout=subprocess.PIPE)
    result_json = decode_result(result_raw)
    if args.verbose:
        print('Done.')

    if args.verbose:
        print('Decoding rubric...')
    rubric = decode_rubric(os.path.join(args.test_dir, RUBRIC_FILENAME))

    if args.verbose:
        print('Generating report...')
    report = generate_report(result_json, rubric)
    print(report)


if __name__ == '__main__':
    main()
