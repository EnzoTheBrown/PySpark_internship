import numpy as np
import pywt
from scipy.spatial import distance
from dummy_spark import SparkContext


class Wavelet:
    def __init__(self, file, context, sample_size):
        self.df = np.genfromtxt(file, delimiter=';')
        self.df = self.df.transpose()
        self.sc = SparkContext(context, 'wavelet')
        self.sample_size = sample_size

        self.file_size = len(self.df[0])
        self.graph_size = int(self.file_size / self.sample_size)
        self.file = file

    def wavelet(self, column):
        print(self.df[column])
        sample_size = self.sample_size
        t = []
        for i in range(1, int(len(self.df[column])/sample_size) - 2):
            t.append(i)
        print(len(t))
        return self.sc.parallelize(t)\
            .map(lambda line: distance.euclidean(pywt.dwt(self.df[column][line*sample_size:(line+1)*sample_size], 'db1')[1]\
                                                 , pywt.dwt(self.df[column][(line + 1)*sample_size:(line + 2)*sample_size], 'db1')[1]))\
            .collect()


#
# sample_size = 1200
# ww = Wavelet('../data/attack.csv', 'local', sample_size)
# print(ww.wavelet(6))