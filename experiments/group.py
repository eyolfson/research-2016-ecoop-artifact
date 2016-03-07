#!/usr/bin/env python

import os

from collections import defaultdict

EXPERIMENTS_DIR = os.path.dirname(os.path.abspath(__file__))

class StackTrace:

    def __init__(self):
        self._data = []

    def add_location(self, path, line, column):
        self._data.append((path, line, column))

    def get_data(self):
        return tuple(self._data)

def group(filename):
    print('# Grouping {}'.format(filename))
    unique_st = defaultdict(int)
    count = 0
    with open(filename, 'r') as f:
        state = 0
        for line in f:
            if state == 0:
                if line.endswith('==WARNING: ConstSanitizer: modification-of-const-value\n'):
                    st = StackTrace()
                    state = 1
                    # Start new stack trace
                # count += 1
            elif state == 1:
                if line.startswith('    #0'):
                    # Add new element to stack trace
                    s = line.split()[-1].split(':')
                    if len(s) != 3:
                        continue
                    st.add_location(s[0], int(s[1]), int(s[2]))
                else:
                    state = 0
                    # End new stack tracea
                    unique_st[st.get_data()] += 1
                    count += 1
    l = []
    for k, v in unique_st.items():
        l.append((v, "{}:{}:{}".format(k[0][0], k[0][1], k[0][2])))
    l.sort(reverse=True)
    for t in l:
        print("{} {}".format(t[0], t[1]))

    print()
    print("Unique Warnings: {}".format(len(unique_st)))
    print("Warnings: {}".format(count))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)
    arg = sys.argv[1]
    for filename in os.listdir():
        if filename.startswith(arg + ".log"):
            group(filename)
