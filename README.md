## black-footed  
- - - -   
##### 1. Logic  
1) Read information from cnf file  
2) Create pid file  
3) Run full backup on local disk  
4) Send backup data to different location  
   - ssh rsync  
   - copy  
5) Clean up local disk backup  
6) Clena up pid file  


##### 2. Condition / Limitation  
- It only runs with single process  
- Systemd
- remote_destination_method=ssh, ssh public key authentication is required.


##### 3. Log / error / notification  
- If backup is running over centain period of time, drop a panic flag
- Log xtrabackup log for later debug


##### 4. Example of cnf  
- location: /etc/black-footed.cnf:  
> pid_file=/tmp/black-footed.pid  
> panic_flag=/tmp/black-footed.panic  
> backup_hour=01  
> local_destination_dir=/tmp/.backup  
> 
> ssh_user=testuser   
> remote_destination_method=copy|ssh  
> remote_destination_host=example.com  
> remote_destination_dir=/tmp/.backup  


##### 5. System requrirement  
- python 2.7  
- pip -- yum install pip  
- [schedule](https://github.com/dbader/schedule)   -- pip install schedule  


##### 6. Reference document  
- [Python and systemd](https://stackoverflow.com/questions/13069634/python-daemon-and-systemd-service)   



