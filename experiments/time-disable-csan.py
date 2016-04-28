#!/usr/bin/env python
#
# Copyright 2016 Jonathan Eyolfson
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import os

EXPERIMENTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(EXPERIMENTS_DIR)
BIN_DIR = os.path.join(BASE_DIR, 'build', 'bin')
COMMAND = 'CC={} CXX={} makepkg -p PKGBUILD-time -s --config {} --nosign --skippgpcheck'.format(
    'clang',
    'clang++',
    os.path.join(EXPERIMENTS_DIR, 'makepkg-disable-csan.conf')
)

if __name__ == '__main__':
    import subprocess
    import sys
    for arg in sys.argv[1:]:
        log_path = os.path.join(EXPERIMENTS_DIR, "{}-build.log".format(arg))
        print(log_path)
        directory = os.path.join(EXPERIMENTS_DIR, arg)
        subprocess.run("rm -rf src pkg *.pkg.tar.xz",
                       shell=True, check=True, cwd=directory)
        try:
            subprocess.run("CSAN_OPTIONS=log_path={} ".format(log_path) + COMMAND,
                           shell=True, check=True, cwd=directory)
        except Exception as e:
            subprocess.run("rm -rf src pkg *.pkg.tar.xz",
                           shell=True, check=True, cwd=directory)
