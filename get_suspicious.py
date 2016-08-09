import pickle 
from pyspark import SparkContext 
import statistics 

pickle_in = open('days_lines.pickle', 'rb') 
res_all = pickle.load(pickle_in) 
TIME_AVG_MAX = 7200 
def manhattan(avg, coordinates):
    (avg1, avg2) = avg
    suspicious = []
    for (x, y) in coordinates:
        if abs(avg1 - x) + abs(avg2 - y) > TIME_AVG_MAX:
            suspicious.append((x, y))
    return suspicious 


def avg_point(coordinates):
    x_min = x_max = 0
    for (x, y) in coordinates:
        x_min += x
        x_max += y
    return x_min / len(coordinates), x_max / len(coordinates) 


def get_median(coordinates):
    x = []
    for coord in coordinates:
        x.append(coord[0])
    y = []
    for coord in coordinates:
        y.append(coord[1])
    return statistics.median(x), statistics.median(y) 

sc = SparkContext('local', 'New App') 
res = sc.parallelize(res_all).map(lambda line: (line[0], get_median(line[1]), line[1]))\
    .map(lambda line: (line[0], line[1], manhattan(line[1], line[2])))\
    .filter(lambda line: len(line[2]) > 0)\
    .collect() 

with open('suspicious_lines.pickle', 'wb') as f:
    pickle.dump(res, f) 

