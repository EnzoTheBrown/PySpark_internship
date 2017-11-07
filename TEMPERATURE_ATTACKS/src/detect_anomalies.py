from pyspark import SparkConext 
import pywt
from scipy.spatial import distance
import matplotlib.pyplot as plt
import re


context = 'local'
filename = 'temperatures.csv'
# the size of the window in seconds
windowsize = 300

sc = SparkContext(context, 'wavelet')
rdd = sc.textFile(filename)
header = rdd.first()


"""
    reducing the dataframe into windows;
    apply the wavelet transform to those windows
"""
wavelet = rdd.filter(lambda line: line :! header)\
        .zipWithIndex()\
        .map(lambda line: (line[1]//windowsize, [ line[0]]))\
        .reduceByKey(lambda a, b: a + b)\
        .map(lambda line: (line[0], pywt.dwt(line[1], 'db1')[1])).cache()


wavelet_left = wavelet.map(lambda line, (line[0]+(1*(1 if line[0]%2 == 0 else 0)), line[1]))\
        .reduceByKey(lambda a, b: distance.euclidean(a, b))

wavelet_right = wavelet.map(lambda line, (line[0]+(1*(1 if line[0]%2 != 0 else 0)), line[1]))\
        .reduceByKey(lambda a, b: distance.euclidean(a, b))

rdd = sc.union([wavelet_right, wavelet_left])

plt.plot(rdd.collect())
plt.show()


sc.stop()






