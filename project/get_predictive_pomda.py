from pyspark import SparkContext
from operator import add
import re
import pickle
from Monk import Monk

monk = Monk()


sc = SparkContext('spark://master:7077', 'My KunFu Is The Best')
res = sc\
    .textFile('hdfs://master:54310/user/hduser1/wifi')\
    .map(lambda line: re.findall(r'[^\s]+', line))\
    .filter(lambda line: len(line) == 7)\
    .map(lambda line: ((line[3], line[5], line[0]), 1))\
    .reduceByKey(add)\
    .map(lambda line: (line[0][0], (line[1], line[0][1], line[0][2])))\
    .groupByKey().mapValues(list)\
    .collect()

with open('listener.pickle', 'wb') as f:
        pickle.dump(res, f)


