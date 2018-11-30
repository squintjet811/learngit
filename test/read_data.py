import scipy.io as matio
import numpy as np
import re
from collections import deque
from MemShare import ShareMemWriter
import os
import time

import spidev
import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("test", help = "real data or fake data", type = int)

args = parser.parse_args()



mat = matio.loadmat('a103l.mat')

data_val = np.array(mat['val'])

print(data_val.shape)

def create_fake_data():

    with open("data_ECG.txt", "r") as fecg:
    ecg_data = []
    for lines in fecg:
        cur_line = lines.strip()
        data_time = re.split(r'\t', cur_line)[0]
        #print(data_time)
        data_val = re.split(r'\t', cur_line)[1]
        data_form = [int(data_time), int(data_val)]
        #print(data_form)
        #ecg_data.append(data_form)
        ecg_data.append(data_val)
np_ecg_data = np.array(ecg_data)
print(ecg_data[0])
sz = 80
data_stack = deque(ecg_data[0 : sz])



#-----------no needed for read signal
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)

#-----------
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) <<4, 0])
    data = ((adc[1]&3)<<8) + adc[2]
    return data








cur_dir = os.getcwd()
cur_path = os.path.join(cur_dir, "memorymap", "sharemem.txt")
name = "sharemem"

with open(cur_path, "r+", encoding="UTF-8") as fshare:
    smw = ShareMemWriter(fshare, np.arange(250), name)
    smw.calculate_size()
    smw.create_mapping()

    data_stack = deque([])
    time_ref = time.time()
    time_cord = 0
    num_it = 40
    for i in range(1000):
        card_adc = ReadChannel(0)
        time_cur = time.time()
        time_cord = time_cord + time_cur - time_ref
        time_ref = time_cur
        x_acc = ReadChannel(1)
        y_acc = ReadChannel(2)
        res_rate = ReadChannel(3)
        data_format = [time_cord, card_adc, x_acc, y_acc, res_rate]
        if(i >= num_it):
            data_stack.popleft()
        data_stack.append(data_format)
        cur_data_interval = np.array(data_stack)
        print(cur_data_interval)

        tic = time.process_time()
        # smw.write_string()
        smw.reset()
        smw.write_data_header()
        smw.write_data(cur_data_interval)
        toc = time.process_time()
        time.sleep(0.1)

