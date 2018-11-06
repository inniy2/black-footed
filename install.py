#!/usr/bin/python
import os
import subprocess

def create_dir():
    directories = ["/etc/black-footed", "/var/run/black-footed", "/var/log/black-footed"]
    for i in range(len(directories)):
      if not os.path.exists(directories[i]):
        os.makedirs(directories[i])  
    print("Directory creation completed.")

def create_file():
    # /etc/black-footed/black-footed.cnf
    p=subprocess.Popen("/bin/cp ./black-footed.cnf /etc/black-footed/", shell=True)
    p=subprocess.Popen("/bin/chown root:root /etc/black-footed/black-footed.cnf", shell=True)
    # /etc/rsyslog.d/black-footed.conf
    p=subprocess.Popen("/bin/cp ./black-footed.conf /etc/rsyslog.d/black-footed.conf", shell=True)
    p=subprocess.Popen("/bin/chown root:root /etc/rsyslog.d/black-footed.conf", shell=True)
    # /usr/lib/systemd/system/black-footed.service
    p=subprocess.Popen("/bin/cp ./black-footed.service /usr/lib/systemd/system/black-footed.service", shell=True)
    p=subprocess.Popen("/bin/chown root:root /usr/lib/systemd/system/black-footed.service", shell=True)
    # /usr/bin/black-footed.py
    p=subprocess.Popen("/bin/cp ./black-footed.py /usr/bin/black-footed.py", shell=True)
    p=subprocess.Popen("/bin/chown root:root /usr/bin/black-footed.py", shell=True)

    print("File creation completed.")
    
def daemon_reload():
    p=subprocess.Popen("/bin/systemctl daemon-reload", shell=True)
    p=subprocess.Popen("/bin/systemctl restart rsyslog.service", shell=True)
    print("Daemon reload completed.")

def main():
    create_dir()
    create_file()
    daemon_reload()

if __name__ == "__main__":
    main()
