import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque



class Plotter:

    def __init__(self, frame_limit = 60):
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = deque([]), deque([])
        self.ln, = plt.plot([], [], 'ro', animated=True)
        self.ani = None
        self.count = 0
        self.frame_limit = frame_limit

    def init(self):
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(-1, 1)
        return self.ln,

    def update(self, frame):
        self.count = self.count + 1

        if self.count > self.frame_limit:
            self.ax.set_xlim(-2 + frame, 2 * np.pi + frame)
            self.ax.set_ylim(-1, 1)
            self.count = 0

        if (len(self.xdata) > 60):
            self.xdata.popleft()
            self.ydata.popleft()

        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.ln.set_data(self.xdata, self.ydata)

        return self.ln,

    def run(self):
        self.ani = FuncAnimation(self.fig, self.update, frames = np.linspace(0, 2 * np.pi, 128),
                init_func = self.init, blit = True)

        plt.show()

def main():
    pl = Plotter()
    pl.run()
    #val = [0, 1, 2, 3, 4, 5]
    #while(True):
       # val = val.pop()
        #pl.run(val)
if __name__ == "__main__":
    main()