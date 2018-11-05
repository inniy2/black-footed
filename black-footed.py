#!/usr/bin/python
import schedule
import os
import sys
import time
import subprocess
import configparser
import shutil
import datetime


# Global variables
global working_dir


# Read variables from .conf
config = configparser.ConfigParser(allow_no_value=True)
config.read_file(open('/etc/black-footed/black-footed.cnf'))
config.sections()


# Create pid file
pid = str(os.getpid())
pidfile = config['default']['pid_file']

if os.path.isfile(pidfile):
  print "%s already exists, exiting" % pidfile
  sys.exit()

file(pidfile, 'w').write(pid)


# Function creating directories
def create_dir():
    directories = [config['default']['local_destination_dir'], config['copy']['remote_destination_dir']]
    for i in range(len(directories)):
      if not os.path.exists(directories[i]):
        os.makedirs(directories[i])  


# Function run full backup
def run_full_backup():
    os.makedirs(config['default']['local_destination_dir']+"/"+working_dir)
    print("I am doing full backup ...")
    print(config['default']['local_destination_dir']+"/"+working_dir + " has been created.")
    sys.stdout.flush()

    p=subprocess.Popen(config['percona']['innobackupex']+
    " --defaults-file="+config['mysql']['defaults_file']+
    " --backup    --compress    --slave-info"+
    " --compress-threads="+config['mysql']['compress_threads']+
    " --user="+config['mysql']['user']+
    " --password="+config['mysql']['password']+
    " --socket="+config['mysql']['socket']+
    " "+config['default']['local_destination_dir']+"/"+working_dir, shell=True)

    time.sleep(120)


# Function copy backup file to local location
def copy_backup_file():
    print("I am doing copy ...")
    sys.stdout.flush()
    shutil.copytree(config['default']['local_destination_dir']+"/"+working_dir,config['copy']['remote_destination_dir']+"/"+working_dir)


# Function ssh backup file to remote location
# TO-DO
def ssh_backup_file():
    print("I am doing ssh ...")
    sys.stdout.flush()


# Function deleting full backup
def delete_local_file():
    print("I am doing deleting local file ...")
    sys.stdout.flush()
    shutil.rmtree(config['default']['local_destination_dir']+"/"+working_dir)


# Function get retention second
def retention_second():
    if int(config['copy']['retention_day_for_copy']) != 0:
      return 86400 * int(config['copy']['retention_day_for_copy'])
    elif int(config['copy']['retention_hour_for_copy']) != 0:
      return 3600  * int(config['copy']['retention_hour_for_copy'])
    else:
      return 60    * int(config['copy']['retention_minute_for_copy'])
     

# Function deleting backup file with retention period option
def delete_copy_file():
    print("I am doing deleting copy file ...")
    if int(config['copy']['retention_day_for_copy']) != 0:
      print("Retention day: " + str(config['copy']['retention_day_for_copy']))
    elif int(config['copy']['retention_hour_for_copy']) != 0:
      print("Retention hour: " + str(config['copy']['retention_hour_for_copy']))
    else:
      print("Retention minute: " + str(config['copy']['retention_minute_for_copy']))
    sys.stdout.flush()

    current_time = time.time()
    for dirname, dirnames, filenames in os.walk(config['copy']['remote_destination_dir']):
      if dirname[len(config['copy']['remote_destination_dir'])+0:].count(os.sep) == 1:
        if ((current_time - os.path.getctime(dirname)) > retention_second() ):
          shutil.rmtree(dirname)
          print(dirname + " has been deleted.")
          sys.stdout.flush()


# Function JOB
def job():
    create_dir()
    global working_dir
    working_dir=datetime.datetime.today().strftime('%Y%m%d%H%M%S')

    print("Backup started...")
    sys.stdout.flush()

    run_full_backup()

    print("Backup completed.")
    sys.stdout.flush()

    copy_backup_file()
    delete_local_file()
    delete_copy_file()

    print("Job completed.")
    print("--------------")
    sys.stdout.flush()


# Job interval setup
if config['default']['backup_daily_time'] != "00:00":
  print("Daily schedule: "+config['default']['backup_daily_time'])
  sys.stdout.flush()
  schedule.every().day.at(config['default']['backup_daily_time']).do(job)
elif int(config['default']['backup_interval_hour']) != 0:
  print("Hourly schedule: "+str(config['default']['backup_interval_hour']))
  sys.stdout.flush()
  schedule.every(int(config['default']['backup_interval_hour'])).hour.do(job)
else:
  print("Minute schedule: "+str(config['default']['backup_interval_minute']))
  sys.stdout.flush()
  schedule.every(int(config['default']['backup_interval_minute'])).minutes.do(job)


# JOB related loop
while 1:
    schedule.run_pending()
    time.sleep(1)
