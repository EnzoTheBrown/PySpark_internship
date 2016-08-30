import pickle
import matplotlib.pyplot as plt
import re
import numpy as np
from Least_squares import mean, least_square

pickle_in = open('../data/wavelet_result.pickle', 'rb')
t = pickle.load(pickle_in)


pickle_in = open('../data/wavelet.pickle', 'rb')
ww = pickle.load(pickle_in)
sample_size = ww.sample_size

legend = re.split(r';','Sensor Impersonation attack;Replay attack;Denial of service attack;Random signal in range;no attack average; no attack')
x = np.array(t[0])

graph_size = ww.graph_size
file_size = ww.file_size
column = 0
for graph in t:
    if column != 2:
        xs = range(0 + graph_size*column, int(file_size / sample_size) + graph_size*column-4)
        print(len(xs), len(graph[1:]))
        plt.scatter(xs, graph[1:])
        plt.plot(xs, graph[1:], label=legend[column])
    column += 1
#this is the mean line of the normal data
mm = mean(t[-1])
plt.plot([0,  int(file_size / sample_size) + graph_size*column], [mm, mm], 'k-', color='k')

mm75 = 0
mm25 = 0
l1 = 0
l2 = 0
for i in t[-1]:
    if i > mm:
        mm75 += i
        l1 += 1
    else:
        mm25 += i
        l2 += 1
mm75 /= l1
mm25 /= l2

plt.plot([0,  int(file_size / sample_size) + graph_size*column], [mm75, mm75], 'k-', color='r')
plt.plot([0,  int(file_size / sample_size) + graph_size*column], [mm25, mm25], 'k-', color='r')


plt.legend()
plt.show()
