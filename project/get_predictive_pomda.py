from pyspark import SparkContext
from operator import add
import re
import pickle
from Monk import Monk

monk = Monk()

def count_repeat(actions):
    old = actions[0][0]
    it = 0
    list = actions[1]
    new_list = []
    for action in list:
        if action != old:
            new_list.append((old, it))
            it = 1
            old = action
        else:
            it += 1
    new_list.append((old, it))
    return [actions[0][0], (actions[0][1], new_list)]

sc = SparkContext('spark://master:7077', 'My KunFu Is The Best')
res = sc\
    .textFile('hdfs://master:54310/user/hduser1/wifi')\
    .map(lambda line: re.findall(r'[^\s]+', line))\
    .filter(lambda line: len(line) == 7)\
    .map(lambda line: ((line[3], line[0]), line[5]))\
    .groupByKey().mapValues(list)\
    .map(lambda line: count_repeat(line))\
    .groupByKey().mapValues(list)\
    .collect()

with open('listener_pomda.pickle', 'wb') as f:
        pickle.dump(res, f)


