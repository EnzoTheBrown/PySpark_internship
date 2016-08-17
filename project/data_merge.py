
import re
import datetime 
import calendar 

class Monk:
    
    @staticmethod
    def convert_h_to_s(h):
        if h is None:
            return -43320
        data = re.split(r':', h)
        return int(data[0])*3600 + int(data[1])*60 + int(data[2])


    @staticmethod
    def convert_s_to_h(s):
        h = str(int(s/3600))
        s %= 3600
        if int(h) < 0:
            return None
        if int(h) < 10:
            h = ('0' + h)
        m = str(int(s/60))
        if int(m) < 10:
            m = ('0' + m)
        s %= 60
        if s > 10:
            s = str(s)
        else:
            s = ('0%i' % s)
        return h+':'+m+':'+s


    @staticmethod
    def get_day_from_date(date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return calendar.day_name[date.weekday()] 



import re 
import pickle 
from pyspark import SparkContext  

from pyspark.mllib.stat import Statistics
import numpy as np
import hashlib

class get_activity:

    def __init__(self):
        str = open('hdfs_connection.yml', 'r').read()
        str = re.split(r'\n', str)
        self.connection = (re.findall(r'file:\s+(.*)',str[1])[0], re.findall(r'context:\s+(.*)', str[0])[0])
        self.sc = SparkContext(self.connection[1], 'My kunfu is the best')

    def Hash_mac():
        ''' **** '''
        self.hash = {}
        str = open('mac_address_wifi', 'r').read()
        str = re.sub(r'\s', r'\n', str)
        addresses = re.split(r'\n', str)
        i = 0
        for add in addresses:
            if add != '': 
                self.hash[add] = i
                i += 1

    def activity(self, address):
	monk = Monk() #wolololo
 
        self.res_all = self.sc\
            .textFile(self.connection[0])\
            .filter(lambda line: address in line)\
            .map(lambda line: re.split(r'\s+', line))\
            .map(lambda line: (line[0], (monk.convert_h_to_s(line[1]), monk.convert_h_to_s(line[1]))))\
            .reduceByKey(self.min_max)\
            .map(lambda line: (monk.get_day_from_date(line[0]), line[1]))\
            .groupByKey()\
            .map(lambda line: (line[0], list(line[1]))).collect() 
        return self.res_all

    @staticmethod
    def same(add1, add2):
        print(add1)
        if add1 == add2:
            return '->'
        else:
            return '<-'

    def get_day_hour(line):
        monk = Monk() #wolololo
        line = re.split(r'\s+', line)
        return [monk.get_day_from_date(line[0]), monk.get_S_from_H(line[1])]

    def get_id_from_mac(mac):
        return D[mac]

    def get_listener(self):
        return self.sc\
            .textFile(self.connection[0])\
            .map(lambda line: re.split(r'\s+', line))\
            .filter(lambda line: len(line) == 6)\
            .map(lambda line: (line[3], line[5]))\
            .groupByKey().mapValues(list).take(100)






    def res(self):
        print(30*'_')
        print(self.res_all)
        print(30*'_')
        return(self.res_all)


    def picklize(self):
        with open('days_lines.pickle', 'wb') as f:
            pickle.dump(self.res_all, f)

    @staticmethod
    def min_max(minmax, coord):
        (x_min, x_max) = minmax
        (x, y) = coord
        if x_min > x:
            x_min = x
        if x_max < y:
            x_max = y
        return x_min, x_max





import re


#str = open('mac_address_wifi', 'r').read()
#str = re.sub(r'\s', r'\n', str)
#addressesI = re.split(r'\n', str)
#for address in addresses:
#    re.sub(r'\s', r'', address)
A = get_activity()
print(A.get_listener())
#addresses = []
#for add in addressesI:
#    if add != '':
#        addresses.append(add)
#for address in addresses:
#    res = A.activity(address)
#    with open('mac_address_activity/'+address+'.pickle', 'wb') as f:
#        pickle.dump(res, f)
#os.system('ls -l mac_address_activity')


