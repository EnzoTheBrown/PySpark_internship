import pywt
from scipy.spatial import distance
from dummy_spark import SparkContext
import re


class Wavelet:
    def __init__(self, context, file, sample_size):
        self.sc = SparkContext(context, 'Wavelet')
        self.file_size = self.sc.textFile(file).count()
        self.sample_size = sample_size
        self.graph_size = int(self.file_size / self.sample_size)
        self.file = file

    def wavelet(self, column, name):
        sample_size = self.sample_size
        sc = self.sc
        link = self.file
        length = self.file_size

        tab = []
        for i in range(0, length):
            tab.append(length - i)

        def get_key(iterator, size):
            key = int(iterator/size)
            iterator += 1
            return key

        rdd = sc\
            .textFile(link)\
            .filter(lambda line: name not in line)\
            .map(lambda line: (get_key(tab.pop(), sample_size), re.split(r';', line)[column]))\
            .groupByKey().mapValues(list)\
            .map(lambda line: (line[0], pywt.dwt(line[1], 'db1')[1]))

        def get_previous_line(line):
            iterator = line[0]
            if iterator == 0:
                prev = rdd.filter(lambda my_line: my_line[0] == iterator).collect()[0][1]
            else:
                prev = rdd.filter(lambda my_line: my_line[0] == iterator - 1).collect()[0][1]
            d = distance.euclidean(line[1], prev)
            return d

        return rdd\
            .map(lambda line: get_previous_line(line))\
            .collect()
