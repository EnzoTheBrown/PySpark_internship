from pyspark import SparkContext

sc = SparkContext('spark://master:7077', 'test')

print sc.parallelize([1, 1, 2, 3]).distinct().collect()
