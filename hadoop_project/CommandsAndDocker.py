import os
import re

class Commands:
    def execcommand(self,
                    container,
                    pattern):
        cmd1 = ' hdfs dfs -put ' + pattern + '* /user/cloudera/a'
        os.system('docker exec ' + container + ' echo #!/bin/sh\n' + cmd1 + ' > tmp')
        os.system('docker exec ' + container + ' chmod 777 tmp')
        cmd = 'docker exec ' + container + ' ./tmp'
        print(cmd1)
        os.system(cmd)