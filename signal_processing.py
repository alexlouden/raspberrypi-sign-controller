from __future__ import division
import time
import pyaudio
import numpy as np
import scipy
import scipy.signal


def bandpower(x, fs, fmin, fmax):
    f, Pxx = scipy.signal.periodogram(x, fs=fs)
    ind_min = scipy.argmax(f > fmin) - 1
    ind_max = scipy.argmax(f > fmax) - 1
    return scipy.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


def scale(x):
    # x *= scale
    # s = 1
    # x = np.exp(x * s) / np.exp(s)
    x = np.log(1+x) / np.log(2)
    x = max(x, 0)  # limits
    x = min(x, 1)
    return x


def list_devices():
    import pyaudio
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(i, dev['name'], dev['maxInputChannels'])
        # (2, u'USB PnP Sound Device: Audio (hw:1,0)', 1L)


class Stream():

    def __init__(self):
        self.open_stream()

    def open_stream(self):

        self.fs = 44100
        update_freq = 20  # Hz
        self.chunk_size = int(self.fs / update_freq)

        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.fs,
            input=True,
            frames_per_buffer=self.chunk_size,
            input_device_index=2)

    def get_chunk(self):
        return np.fromstring(self.stream.read(self.chunk_size, exception_on_overflow=False), dtype=np.int16)

    def process_chunk(self):
        chunk = self.get_chunk()

        bass = bandpower(chunk, self.fs, 20, 250) / 2000
        mid = bandpower(chunk, self.fs, 250, 2000) / 500

        return scale(bass), scale(mid)

    def loop(self):
        while True:
            t = time.time()
            b, m = self.process_chunk()
            elapsed = time.time() - t
            if elapsed < 1/20:
                time.sleep(int(elapsed - 0.2) * 1000)
            # print('{:.09f}'.format(s))
            print('X'*int(b*100))
            print('|'*int(m*100))

if __name__ == '__main__':
    s = Stream()
    s.loop()
