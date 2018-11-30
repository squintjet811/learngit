from biosppy import storage
from biosppy.signals import ecg

import numpy as np

signal, mdata= storage.load_txt('ecg.txt')
out = ecg.ecg(signal = signal, sampling_rate=1000, show=True)