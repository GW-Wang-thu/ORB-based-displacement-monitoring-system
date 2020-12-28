import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import multiprocessing
import time

class ploter:

    def __init__(self, num_wind, num_point):
        self.num_wind = num_wind
        self.num_point = num_point

        self._xlabel = range(0, self.num_point, 1)
        self.y = multiprocessing.Manager().list([[]])
        self._p = multiprocessing.Process(target=self._plot, args=self.y)
        self._p.start()

    def plot(self, y):
        self.y = y
        # self._p.terminate()
        # self._p = multiprocessing.Process(target=self._plot)
        # self._p.start()

    def _plot(self, y):
        self.__initwind__()
        timer = self._fig.canvas.new_timer(interval=100)
        timer.add_callback(self.refresh)
        timer.start()
        plt.show()

    def __initwind__(self):
        self._fig, self._ax = plt.subplots(self.num_wind, 1)
        for i in range(self.num_wind):
            # exec("self._ax["+str(i+1)+"] = plt.subplot("+str(self.num_wind)+str(1)+str(i+1)+")")
            exec("self._ax["+str(i)+"].grid(True)")
            exec("self._ax["+str(i)+"].set_xlabel('Time interval/step', fontsize=14)")
            exec("self._ax["+str(i)+"].set_ylabel('Displacement/Pixels', fontsize=14)")
            exec("self._ax["+str(i)+"].set_title('Point '+str(i+1), fontsize=18)")

    def refresh(self):
        print("Refresh called")
        out_y = self.y.copy()
        print(self.y)
        for i in range(self.num_wind):
            if i >= len(out_y):
                out_y.append([0] * self.num_point)
            out_y_step = [0] * self.num_point + out_y[i]
            exec("self._ax["+str(i)+"].plot(self._xlabel, out_y_step[-self.num_point:], 'g-')")


class plot:

    def __init__(self, num_wind, num_point):
        self.num_wind = num_wind
        self.num_point = num_point

        self._xlabel = range(0, self.num_point, 1)
        self.y = [[]]

    def refresh(self):
        out_y = self.y.copy()
        print(self.y)
        plt.clf()
        plt.ion()
        plt.suptitle("Displacements Monitor", fontsize=30)
        for i in range(self.num_wind):
            if i >= len(out_y):
                out_y.append([0] * self.num_point)
            out_y_step = [0] * self.num_point + out_y[i]
            exec("self.graphic" + str(i+1) + " = plt.subplot(" + str(self.num_wind) + ", 1, " + str(i+1) + ")")
            exec("self.graphic" + str(i+1) + ".set_title('Point '+str(i))")  # 添加子标题
            exec("self.graphic" + str(i+1) + ".set_xlabel('Time Interval', fontsize=10)")  # 添加轴标签
            exec("self.graphic" + str(i+1) + ".set_ylabel('Displacement/Pixels', fontsize=10)")
            # plt.plot()
            # exec("self.graphic"+str(i)+" = plt.subplot("+str(self.num_wind)+", 1, "+str(i)+")")
            plt.plot(self._xlabel, out_y_step[-self.num_point:], 'g-')  # 等于agraghic.plot(ax,ay,'g-')

        # 图表2
        # bx.append(num)
        # by.append(g1)
        # bgraghic = plt.subplot(2, 1, 2)
        # bgraghic.set_title('子图表标题2')
        # bgraghic.plot(bx, by, 'r^')



if __name__ == "__main__":
    plotr = plot(num_wind=4, num_point=100)
    plotr.y = [[1, 2, 2, 2, 2, 2], [3, 3, 2, 2, 4, 5, 5, 6, 2, 1]]
    plotr.refresh()
    plt.pause(0.5)
    plotr.y = [[2, 2,2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,6,1, 2, 2, 2, 2, 2], [3, 3, 22,2,2,2,22,2,2,2,2,2,2,2,2, 2, 4, 5, 5, 6, 2, 1]]
    plotr.refresh()
    plt.pause(0.5)
    plotr.y += [[1, 2, 2, 2,3,3,3,3,3,3,3,3,3,3,3,3,4,5,5,6,6,7,8,8,2, 2], [3, 3, 4,5,6,8,3,4,5,6,8,2, 2, 4, 5, 5, 6, 2, 1]]
    plotr.refresh()
    plt.pause(0.5)
    plotr.y = [[1, 2, 2, 2, 3,3,3,3,4,5,6,7,8,9,0,2, 2], [3, 3, 2, 2, 4, 5, 5, 6, 2, 1]]
    plotr.refresh()
    plt.pause(0.5)
    #
    # plotr.plot(y=[[1, 2, 2, 2, 2, 2], [3, 3, 2, 2, 4, 5, 5, 6, 2, 1]])
    # print("here1, plotr.y: ", plotr.y)
    # time.sleep(5)
    # plotr.plot(y=[[2, 2,2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,6,1, 2, 2, 2, 2, 2], [3, 3, 22,2,2,2,22,2,2,2,2,2,2,2,2, 2, 4, 5, 5, 6, 2, 1]])
    # print("here2, plotr.y: ", plotr.y)
    # time.sleep(2)
    # plotr.plot(y=[[1, 2, 2, 2,3,3,3,3,3,3,3,3,3,3,3,3,4,5,5,6,6,7,8,8,2, 2], [3, 3, 4,5,6,8,3,4,5,6,8,2, 2, 4, 5, 5, 6, 2, 1]])
    # print("here3, plotr.y: ", plotr.y)
    # time.sleep(2)
    # plotr.plot(y=[[1, 2, 2, 2, 3,3,3,3,4,5,6,7,8,9,0,2, 2], [3, 3, 2, 2, 4, 5, 5, 6, 2, 1]])



class Ploter:
    def __init__(self, maxnum_window=1, num_point=100, interval=5000):
        self.num_point = num_point
        self.maxnum_window = maxnum_window
        self.y = []
        self.recorder = 0
        self._fig, self._ax = plt.subplots()
        plt.show()
        self.__refresh__()

    def __refresh__(self):
        y = self.y.copy()
        for i in range(self.maxnum_window):
            self._ax.set_ylim([-5, 5])
            self._ax.set_xlim([0, self.num_point])
            self._ax.grid(True)
            self._line_y, = self._ax.plot(range(self.num_point), [0] * self.num_point, label='P0int output',
                                          color='cornflowerblue')
            self._ax.legend(loc='upper center', ncol=4, prop=font_manager.FontProperties(size=10))
            plt.subplot(self.maxnum_window, 1, i + 1)
            if i >= len(y):
                y.append([0] * self.num_point)
            out_y = [0] * self.num_point + y[i]
            out_y = out_y[-self.num_point:]
            self._line_y.set_ydata(out_y)
            self._ax.draw_artist(self._line_y)
            self._ax.figure.canvas.draw()