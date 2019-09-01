#!/usr/bin/env python
from migrate.versioning.shell import main
from os import environ


if __name__ == '__main__':
    uri = environ.get('DATABASE_URL') or 'postgresql://postgres:cesar420@localhost/camporota'
    main(repository='migrations', url=uri, debug='False')
