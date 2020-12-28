import matplotlib.pylab as plt
import numpy as np
import multiprocessing

class Ploter:

    def __init__(self, num_wind, num_point):
        self.num_wind = num_wind
        self.num_point = num_point

        self._xlabel = range(0, self.num_point, 1)
        self.y = [[]]

    def refresh(self):
        out_y = self.y.copy()
        plt.clf()
        plt.ion()
        plt.suptitle("Displacements Monitor", fontsize=15)
        while self.num_wind > len(out_y):
            out_y.append([0] * self.num_point)
        for i in range(self.num_wind):
            out_y_step = [0] * self.num_point + out_y[i-self.num_wind+len(out_y)]
            exec("self.graphic" + str(i+1) + " = plt.subplot(" + str(self.num_wind) + ", 1, " + str(i+1) + ")")
            exec("self.graphic" + str(i+1) + ".set_title('Point '+str(i))")  # 添加子标题
            exec("self.graphic" + str(i+1) + ".set_xlabel('Time Interval', fontsize=10)")  # 添加轴标签
            exec("self.graphic" + str(i+1) + ".set_ylabel('Displacement/Pixels', fontsize=10)")
            # plt.plot()
            # exec("self.graphic"+str(i)+" = plt.subplot("+str(self.num_wind)+", 1, "+str(i)+")")
            plt.plot(self._xlabel, out_y_step[-self.num_point:], 'g-')  # 等于agraghic.plot(ax,ay,'g-')

#
# class Analyst:
#
#     def __init__(self, shared_signal_pointer):
#         self.signal = shared_signal_pointer
#         self.thread = multiprocessing.
#
#     def __alarm__(self, level):
#
#     def frequency_analyse(self, params):
#
#     def denoise(self, windowsize):
#
#     def save(self, interval=10):