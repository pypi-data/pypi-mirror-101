#!/usr/bin/env python3

import sys

from .linter_quotes import Linter


def log(s, *args):
    if args:
        s = s.format(*args)
    print(s)


def main():
    linter = Linter()
    for a in sys.argv[1:]:
        log('Checking {}', a)
        if not linter.allow(a):
            log('  Linter REJECTS!')
            continue
        for e in linter.run(a):
            log('  FOUND: {}', e)


if __name__ == '__main__':
    main()
