import re 
import datetime 
import calendar 
import pickle 
from pyspark import SparkContext 

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

monk = Monk() 

def min_max(minmax, coord):
    (x_min, x_max) = minmax
    (x, y) = coord
    if x_min > x:
        x_min = x
    if x_max < y:
        x_max = y
    return x_min, x_max 

sc = SparkContext('local', 'New App') 
res_all = sc\
    .textFile('../../../Wi-FiDatabase/4ngram_ch6_time_type_ta_ra_da_sa.csv')\
    .filter(lambda line: '00:19:07:8d:ed:53' in line)\
    .map(lambda line: re.split(r'\s+', line))\
    .map(lambda line: (line[0], (monk.convert_h_to_s(line[1]), monk.convert_h_to_s(line[1]))))\
    .reduceByKey(min_max)\
    .map(lambda line: (monk.get_day_from_date(line[0]), line[1]))\
    .groupByKey()\
    .map(lambda line: (line[0], list(line[1]))).collect() 

with open('days_lines.pickle', 'wb') as f:
    pickle.dump(res_all, f)


