import os
import numpy as np
import time
from MemShare import ShareMemReader
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import RPi.GPIO as GPIO
import subprocess


cur_dir = os.getcwd()
print(cur_dir)
cur_path = os.path.join(cur_dir, "memorymap", "sharemem.txt")
name = "sharemem"
'''
def buzz(bpm):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    print("convert to int", bpm /60)
    if(bpm == 0):
        bpm = 0.01
    pwm = GPIO.PWM(18,bpm /60)
    pwm.start(50)
    time.sleep(5)
    GPIO.cleanup()
'''

def detect_shake(data_acc, thre = 3):
    data_acc_np =np.array(data_acc)
    data_std = np.std(data_acc_np)
    print("the deviation is ", data_std)
    b_return = False
    if data_std > thre:
        b_return = True

    return b_return

def count_peak(data_adc, thre = 2):
    #input:
    # data_adc array
    # data_time array

    edge_hit = False
    beat_count = 0
    for i in range(len(data_adc)):
        if (data_adc[i] > thre and not edge_hit):
            beat_count = beat_count + 1
            edge_hit = True
        if (data_adc[i] < thre and edge_hit):
            edge_hit = False

    return beat_count

def count_bpm(data_adc, data_time, thre = 2):

    time_diff = data_time[-1] - data_time[0]
    beat_total = count_peak(data_adc, thre)
    bpm = beat_total / time_diff
    return bpm

with open(cur_path, "r+", encoding="UTF-8") as fshare:

    smr = ShareMemReader(fshare, name)
    print("start reading --------------------------")
    smr.create_mapping()

    smr.read_data_size()

    smr.create_mapping()

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    cnt = 0


    line, = ax1.plot([0], [0])
    text = ax1.text(0.97, 0.97, "", transform=ax1.transAxes, ha="right", va="top")

    #plt.ylim(0, 25)
    plt.xlim(0, 300)
    last_time = {0: time.time()}
    plt.ylim(-1000, 1000)



    def animateinit():  # tells our animator what artists will need re-drawing every time
        return line, text


    def animate(i):
        tic = time.clock()
        smr.create_mapping()
        smr.copy_buffer()
        smr.read_data_header()
        result = smr.read_data_body()
        result = np.array(result).reshape(-1, 5)
        time_result = result[:, 0].tolist()
        adc_result = result[:, 1].tolist()
        #bpm_result = count_bpm(adc_result, time_result)
        #result_mean = np.mean(result)
        #result_biased = np.ones()
        global data_adc_beat_measure
        global data_adc_time_measure
        global ps
        print("current frame", i)
        if(i % 200 == 0):
            data_adc_beat_measure = []
            data_adc_time_measure = []

        else:
            data_adc_beat_measure.append(adc_result[-1])
            data_adc_time_measure.append(time_result[-1])
            if(i % 200 == 199):
                if ps is not None:
                    try:
                        ps.kill()
                        print("kill previous call process")
                bpm_result = count_bpm(data_adc_beat_measure, data_adc_time_measure)
                sleep_time = 5
                command_promt = "python3 hapitic.py" + " " + str(int(bpm_result))  + " " + str(sleep_time)
                ps = subprocess.Popen(command_promt)
                print("beat is ", bpm_result * 60)
                print("beat is ", bpm_result * 60)
                #buzz(bpm_result)
            
        toc = time.clock()
        #print(i)
        #print(result)
        #print(result.shape)
        #print(bpm_result * 60)
        #print("time", 1000 * (tic - toc))
        smr.reset()
        smr.close()
        line.set_data(result[:, 0], result[:, 1])

        #print(result[:, 0].shape)
        #print(result[:, 1].shape)
        new_time = time.time()
        text.set_text("{0:.2f} fps".format(1. / (new_time - last_time[0])))
        last_time.update({0: new_time})
        return line, text  # return the updated artists

    # inform the animator what our init_func is and enable blittingi
    data_adc_beat_measur = []
    data_adc_time_measure = []
    ps = None
    ani = animation.FuncAnimation(fig, animate, interval= 100, frames = None, init_func=animateinit, blit=True)
    plt.show()
