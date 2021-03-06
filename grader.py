#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from batch.constants import *

ELM_CACHE_PATH = os.path.join(ELM_TESTER_DIR, 'tests/elm-stuff/build-artifacts/0.18.0/user')


class BrokenTestsError(Exception):
    pass


class TestingFailureError(Exception):
    pass


def decode_result(proc):
    """
    Parses the testing result into a Python object.
    :param proc: CompletedProcess
    :return: a list of dictionaries
    """
    lines = proc.stdout.decode('utf-8').split('\n')
    result = []
    for line in lines:
        if len(line) > 0:
            result.append(json.loads(line))
    return result


def count_tests(tests_path):
    """
    Counts the number of tests in an Elm tests file.
    :param tests_path: str
    :return: int
    """
    with open(tests_path) as f:
        ret = 0
        for line in f.readlines():
            if 'test "' in line:
                ret += 1
        return ret


def decode_status(event):
    if event['status'] == 'pass':
        return True
    elif event['status'] == 'fail':
        return False
    else:
        print('Bad test result: ', event['status'], file=sys.stderr)
        return False


def intify(x):
    """
    Make x an integer if it is an integer
    :param x: float
    :return: int or float
    """
    if x.is_integer():
        return int(x)
    return x


def generate_report(test_result, n_tests):
    """
    Generates a test report based on test result.
    :param test_result: list, test result
    :param n_tests: int, expected number of tests
    :return: (string, int), (report text, points)
    """
    # Pre-processing
    test_events = list(filter(lambda e: e['event'] == 'testCompleted', test_result))

    if len(test_events) != n_tests:
        raise TestingFailureError("Wrong number of test results; expecting {0}, got {1}".format(
            n_tests, len(test_events)))

    # Initialization
    report = []
    total = 0.0
    my_total = 0.0
    current_suite = None
    subtotal = 0.0
    my_subtotal = 0.0

    # Utility functions
    def conclude_suite():
        nonlocal report, total, my_total, current_suite, subtotal, my_subtotal
        if current_suite is not None:
            # Conclude previous test suite
            report.append('')
            report.append("  Subtotal: {0} / {1}".format(intify(my_subtotal), intify(subtotal)))
            report.append('')
            total += subtotal
            my_total += my_subtotal

    # Iterate over test results
    for event in test_events:
        # TODO: support arbitrary test suite depth
        # Extract test metadata
        if len(event['labels']) != 3:
            raise BrokenTestsError('Invalid test labels')
        test_suite = event['labels'][1]
        test_name_list = event['labels'][2].split('@')
        if len(test_name_list) != 2:
            raise BrokenTestsError("Invalid test name '{0}'; must include points".format(test_name_list[0]))
        test = test_name_list[0].strip()
        points = intify(float(test_name_list[1]))

        if test_suite != current_suite:
            conclude_suite()

            # Open new test suite
            subtotal = 0.0
            my_subtotal = 0.0
            current_suite = test_suite
            report.append("Test Suite: {0}".format(test_suite))
            report.append('')

        # Handle current test
        status = decode_status(event)
        my_points = points if status else 0
        subtotal += points
        my_subtotal += my_points
        report.append("  - Test Case {0}: {1} / {2}".format(test, my_points, points))

    # Conclude the last test suite
    conclude_suite()

    # Conclude the test report
    report_name = test_events[0]['labels'][0]
    report = ["{0} Total Score: {1} / {2}".format(report_name, intify(my_total), intify(total)), ''] + report
    report_text = '\n'.join(report)
    return report_text, my_total


def grade(argv):
    """
    Main routine.
    :param argv: list, command line arguments
    :return: int, the grade
    """
    parser = argparse.ArgumentParser(description='Set up and run Elm automated testing.')
    parser.add_argument('test_dir', help='directory containing test files')
    parser.add_argument('-d', '--dependencies', nargs='*', help='dependent module file paths')
    parser.add_argument('-o', '--output', help='output file, default to stdout')
    parser.add_argument('-e', '--expose', action='store_true', help='force module files to expose everything')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args(args=argv)

    if args.verbose:
        print("Preparing to run test suite '{0}'...".format(args.test_dir))

    if os.path.exists(ELM_CACHE_PATH):
        shutil.rmtree(ELM_CACHE_PATH)
    shutil.copy(os.path.join(args.test_dir, TESTS_FILENAME), os.path.join(ELM_TESTER_DIR, 'tests'))

    copied_dependencies_path = []
    if args.dependencies is not None:
        for dep_path in args.dependencies:
            dep_filename = os.path.basename(dep_path)
            copied_dep_path = shutil.copy(dep_path, os.path.join(ELM_TESTER_DIR, 'tests'))
            copied_dependencies_path.append(copied_dep_path)
            if args.expose:
                # Expose all Elm functions in module
                with open(copied_dep_path) as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if line.startswith('module '):
                            lines[i] = "module {} exposing (..)".format(dep_filename[:-4])
                            break
                with open(copied_dep_path, 'w') as f:
                    for line in lines:
                        f.write(line)

    if args.verbose:
        print('Running tests...', end='')

    try:
        # proc = subprocess.run(['elm-test'], cwd=ELM_TESTER_DIR)
        proc = subprocess.run(['elm-test', '--report', 'json'], cwd=ELM_TESTER_DIR, stdout=subprocess.PIPE)
        result_json = decode_result(proc)
        if args.verbose:
            print(' done.')

        if args.verbose:
            print('Analyzing tests...')
        n_tests = count_tests(os.path.join(ELM_TESTER_DIR, 'tests', TESTS_FILENAME))

        if args.verbose:
            print('Generating report...')

        try:
            report, score = generate_report(result_json, n_tests)
        finally:
            if args.verbose:
                print('Cleaning up...')
            os.remove(os.path.join(ELM_TESTER_DIR, 'tests', TESTS_FILENAME))
            for copied_dep_path in copied_dependencies_path:
                os.remove(copied_dep_path)

        if args.output is not None:
            print(args.output)
            with open(args.output, 'w') as f:
                print(report, file=f)
        else:
            print(report)
        return score

    except IndexError:
        print('Error: incomplete test result possibly due to crash')
        return 0


def main():
    grade(sys.argv[1:])


if __name__ == '__main__':
    main()
