#!/usr/bin/env python

import os

EXPERIMENTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(EXPERIMENTS_DIR)
BIN_DIR = os.path.join(BASE_DIR, 'build', 'bin')
COMMAND = 'CC={} CXX={} makepkg -s --config {} --nosign --skippgpcheck'.format(
    'clang',
    'clang++',
    os.path.join(EXPERIMENTS_DIR, 'makepkg.conf')
)

if __name__ == '__main__':
    import subprocess
    import sys
    for arg in sys.argv[1:]:
        log_path = os.path.join(EXPERIMENTS_DIR, "{}-build.log".format(arg))
        print(log_path)
        directory = os.path.join(EXPERIMENTS_DIR, arg)
        subprocess.run("CSAN_OPTIONS=log_path={} ".format(log_path) + COMMAND,
                       shell=True, check=True, cwd=directory)
