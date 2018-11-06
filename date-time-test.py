#!/usr/bin/python
import datetime
import time
import os

print(datetime.datetime.now())
print(datetime.datetime.now().isoformat())
print(datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
print(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))


current_time = time.time()
print(current_time)
creation_time = os.path.getctime("/tmp/mount/.backup/20181105104721")
print(creation_time)
print(current_time - creation_time)


#for dirname, dirnames, filenames in os.walk('/tmp/mount/.backup'):
#  if dirname[len('/tmp/mount/.backup')+1:].count(os.sep) < 2:
#    for dir in dirnames:
#      print(dirname[len('/tmp/mount/.backup')+1:].count(os.sep))
#      print(os.path.join(dirname,dir))



current_time = time.time()
for dirname, dirnames, filenames in os.walk('/tmp/mount/.backup'):
  if dirname[len('/tmp/mount/.backup')+0:].count(os.sep) == 1:
     if ((current_time - os.path.getctime(dirname)) > ( 60 * 80)):
       print(dirname)


if ((current_time - creation_time) > (60 * 2)):
  print ("old")
else:
  print ("else")
