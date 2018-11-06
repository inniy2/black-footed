#!/usr/bin/python

import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read_file(open('/etc/black-footed.conf'))
config.sections()
print(config['default']['pid_file'])
