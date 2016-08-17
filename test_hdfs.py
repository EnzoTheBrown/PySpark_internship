from pyspark import SparkContext

sc = SparkContext('spark://master:7077', 'test_hdfs')

lines = sc.textFile('hdfs://master:54310/user/hduser1/wifi').first()
print lines
