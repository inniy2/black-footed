#!/usr/bin/python
import schedule
import os
import sys
import time
import subprocess

pid = str(os.getpid())
pidfile = "/tmp/foo.pid"

if os.path.isfile(pidfile):
  print "%s already exists, exiting" % pidfile
  sys.exit()
file(pidfile, 'w').write(pid)


def job():
    print("I'm working...")
    sys.stdout.write("I'm showing\n")
    sys.stdout.flush()


schedule.every(1).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)


while 1:
    schedule.run_pending()
    time.sleep(1)
