import logging
import os

class myLogs:
    def get_cluster_hardware(self,
                             container):
        os.system("docker exec " + container + " ls /var/log/impala/ > logs1")
        os.system("docker exec " + container + " cat /var/log/impala/*INFO* > logs2")
        #it seems to only return your CPU model and the physical memory line.


LL = myLogs()
LL.get_cluster_hardware('eceeeb983e30')