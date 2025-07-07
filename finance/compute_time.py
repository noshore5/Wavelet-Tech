from multiprocessing import Process, Queue
import numpy as np
import tracemalloc
import pycwt
import fcwt
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import pickle


def wavelet_coherence(signal1, signal2, highest_freq, lowest_freq, nfreqs, sampling_rate):
    freqs, coeffs1 = fcwt.cwt(signal1, sampling_rate, lowest_freq, highest_freq, nfreqs,scaling='log')
    _, coeffs2 = fcwt.cwt(signal2, sampling_rate, lowest_freq, highest_freq, nfreqs,scaling='log')
    
    S1 = np.abs(coeffs1) ** 2
    S2 = np.abs(coeffs2) ** 2
    S12 = coeffs1 * np.conj(coeffs2)

    def smooth(data, sigma=(2, 2), mode='nearest'):
        return gaussian_filter(data, sigma=sigma, mode=mode)

    S1_smooth = smooth(S1)
    S2_smooth = smooth(S2)
    S12_smooth = smooth(np.abs(S12) ** 2)

    coherence = S12_smooth / (np.sqrt(S1_smooth) * np.sqrt(S2_smooth))
    return coherence, freqs
mother = pycwt.Morlet(6)

# Dummy test data
sampling_rate = 8000
nfreqs = 100
t = np.arange(0, 1, 1 / sampling_rate)
noise1 =np.random.randn(len(t))
noise2 =np.random.randn(len(t))
def compute_wavelet_params(f_min, f_max, nscales, dt, f_c=0.8125):
    a_min = f_c / f_max
    a_max = f_c / f_min
    dj = np.log2(a_max / a_min) / nscales
    s0 = a_min * dt
    J = nscales - 1
    return dj, s0, J

def run_coherence_a(q,label,noise1,noise2,nfreqs):
    tracemalloc.start()
    coh, _ = wavelet_coherence(noise1, noise2, 4000, 200, nfreqs, sampling_rate)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    q.put(peak/1024/1024)
    #q.put(f"Coherence A: Peak RAM = {peak / 1024 / 1024:.2f} MB")

def run_coherence_b(q,label,noise1,noise2,nfreqs):

    dj, s0, J = compute_wavelet_params(200, 4000, nfreqs, 1 / sampling_rate)

    tracemalloc.start()
    coh2, *_ = pycwt.wct(noise1, noise2, 1 / sampling_rate, dj=dj, s0=s0, J=J, wavelet=mother, sig=False)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    q.put(peak/1024/1024)
    #q.put(f"Coherence B: Peak RAM = {peak / 1024 / 1024:.2f} MB")

sampling_rate = 8000
nfreqs = 100
duration = 3
t = np.arange(0, duration, 1 / sampling_rate)
noise1 =np.random.randn(len(t))
noise2 =np.random.randn(len(t))
'''
if __name__ == "__main__":

    q1 = Queue()
    q2 = Queue()

    p1 = Process(target=run_coherence_a, args=(q1, 'Test A', noise1, noise2, nfreqs))
    p2 = Process(target=run_coherence_b, args=(q2, 'Test B', noise1, noise2, nfreqs))
    p1.start()
    p1.join()

    p2.start()
    p2.join()

    print(q1.get())
    print(q2.get())
'''

if __name__ == "__main__":
    durations = np.linspace(1, 10, 20)
    peaks_a = []
    peaks_b = []
    nfreqs = np.array([50,100,150,200,250,300,350,400,450,500])
    
    for n in nfreqs:
        qa, qb = Queue(), Queue()
        #t = np.arange(0, d, 1 / sampling_rate)
        t = np.arange(0, 1, 1 / sampling_rate)
        noise1 =np.random.randn(len(t))
        noise2 =np.random.randn(len(t))
        n = int(n)
        pa = Process(target=run_coherence_a, args=(qa, 'Test A', noise1, noise2, n))
        pb = Process(target=run_coherence_b, args=(qb, 'Test B', noise1, noise2, n))

        pa.start()
        pb.start()
        pa.join()
        pb.join()

        peaks_a.append(qa.get())
        peaks_b.append(qb.get())
        
    peaks = [peaks_a,peaks_b]
    print(peaks)
    # Save the `tunes` object to a file
    #with open('peaks.pkl','wb') as file:
    #    pickle.dump(peaks, file)

