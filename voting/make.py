#!/usr/bin/env python3

from glob import glob
import os
from string import Template
import subprocess

HTML_DIR = './html'
SUBMISSIONS_DIR = './submissions'
FOOTER_PATH = os.path.join(HTML_DIR, 'footer.html')
HEADER_PATH = os.path.join(HTML_DIR, 'header.html')
TEMPLATE_PATH = os.path.join(HTML_DIR, 'template.html')
OUTPUT_PATH = 'index.html'
SUBMISSIONS = ['18481', '77377', '91019', '76367', '15551', '19891', None, '98389', '37273', '74047', '30103', '94849', '94949', '78787', '79697', '96469', '38183', '93139', '95959', '96769', '30803', '74747', '96269', '36563', '16061', '94649', '70207', '17471', '35153', '71917', '13931', '11411', '93239', '14741', '73637', '13331', '97379', '76667', '19991', '31513', '97579', '73037', '37573', '10501', '30403', '13831', '11311']


def get_thumbnail(submission_number):
    """
    Find the thumbnail image and return its path
    :param submission_number: str
    :return: str
    """
    for file in glob(os.path.join(SUBMISSIONS_DIR, submission_number, 'ThumbPi.*')):
        return file
    return 'http://placehold.it/200x200'


def main():
    with open(HEADER_PATH) as header_file, open(TEMPLATE_PATH) as template_file, \
            open(FOOTER_PATH) as footer_file, open(OUTPUT_PATH, 'w') as out_file:
        header = header_file.read()
        footer = footer_file.read()
        template_str = template_file.read()
        template = Template(template_str)

        out_file.write(header)
        for number in SUBMISSIONS:
            if number is None:
                continue
            thumbnail_path = get_thumbnail(number)
            section = template.substitute({'submission_number': number, 'thumbnail_path': thumbnail_path})
            out_file.write(section)
        out_file.write(footer)
        subprocess.call(['open', OUTPUT_PATH])


if __name__ == '__main__':
    main()
