from Wavelet_parallelize import Wavelet
import pickle


sample_size = 1200
ww = Wavelet('../data/attack.csv', 'local', sample_size)

t = []
for i in range(0, 6):
    t.append(ww.wavelet(i))

with open('../data/wavelet_result.pickle', 'wb') as f:
    pickle.dump(t, f)

with open('../data/wavelet.pickle', 'wb') as f:
    pickle.dump(ww, f)
