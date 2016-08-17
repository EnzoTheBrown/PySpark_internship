from pyspark import SparkContext
import re
import pickle



sc = SparkContext('spark://master:7077', 'My KunFu Is The Best')
res = sc\
    .textFile('hdfs://master:54310/user/hduser1/wifi')\
    .map(lambda line: re.findall(r'[^\s]+', line))\
    .filter(lambda line: len(line) == 7)\
    .map(lambda line: (line[3], line[5]))\
    .distinct()\
    .groupByKey().mapValues(list)\
    .collect()




with open('listener.pickle', 'wb') as f:
        pickle.dump(res, f)



