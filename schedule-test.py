#!/usr/bin/python
import schedule
import os
import sys
import time
import subprocess
import configparser

# Read variables from .conf
config = configparser.ConfigParser(allow_no_value=True)
config.read_file(open('/etc/black-footed.conf'))
config.sections()

# Create pid file
pid = str(os.getpid())
pidfile = config['default']['pid_file']

if os.path.isfile(pidfile):
  print "%s already exists, exiting" % pidfile
  sys.exit()
file(pidfile, 'w').write(pid)


def create_dir():
    directories = [config['default']['local_destination_dir'], config['copy']['remote_destination_dir']]
    for i in range(len(directories)):
      if not os.path.exists(directories[i]):
        os.makedirs(directories[i])  

def run_full_backup():
    print("I am doing full backup ...")

def copy_backup_file():
    print("I am doing copy ...")

def ssh_backup_file():
    print("I am doing ssh ...")


def job():
    create_dir()
    print("Backup started...")

    print("Backup completed.")
    sys.stdout.flush()


if config['default']['backup_daily_time'] == "00:00":
  schedule.every(int(config['default']['backup_interval_minute'])).minutes.do(job)
else:
  #schedule.every().hour.do(job)
  schedule.every().day.at(config['default']['backup_daily_time']).do(job)



while 1:
    schedule.run_pending()
    time.sleep(1)
