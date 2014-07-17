#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='sqlite:///sylloge_of_codes.sqlite', debug='False', repository='repository')
