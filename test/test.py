import wfdb
from wfdb import processing
import matplotlib.pyplot as plt
import numpy as np
from MemShare import *


class ECGDataProcess:

    def __init__(self, data = 0, threshold = 0, size = 60):
        self.data = data
        self.list_stack = []
        self.size = size
        self.threshold = threshold
        self.ani,  = plt.plot([], [])

    def preprocesing(self):

        #To Do

        return 0

    def read_data(self):

        #To do
        for i in range(self.size):
            self.list_stack.append(self.data)


    def update_data(self):

        #To do
        self.list_stack.pop()
        self.list_stack.append(self.data)

    def calculate_peak(self):

        np_matrix = np.array(self.list_stack)
        np.argsort(np_matrix)
        np_data_filter = np.where(np_matrix > self.threshold)
        np_matrix_sz = np_data_filter.shape[0]

    def plot(self):

        self.ani.set_xdata()
        self.ani.set_ydata()
        plt.draw()



        return 0


def main():

    edp = ECGDataProcess()




if __name__ == "__main__":
    main()



