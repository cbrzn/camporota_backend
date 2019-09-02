#!/usr/bin/env python
from migrate.versioning.shell import main
from os import environ


if __name__ == '__main__':
    uri = environ.get('DATABASE_URL') or 'postgresql://postgres:cesar420@localhost/camporota'
    # prod = 'postgres://vczqpoxvzftnfn:c56ef4f4653753b8132867c4f5330d9bbc0693875952a735e7c0ddca72e3a6c2@ec2-54-228-246-214.eu-west-1.compute.amazonaws.com:5432/d2mktdfobkr16q'
    print(uri)
    main(repository='migrations', url=uri, debug='False')
