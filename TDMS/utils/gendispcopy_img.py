import cv2
import numpy as np

#
# def gendispcopy_img(img, disp=[0, 0]):
#     refimg = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
#     defimg = np.zeros(shape=refimg.shape, dtype="uint8")
#     if disp[0] >= 0:
#         defimg[disp[0]:, :] = refimg[:-disp[0], :]
#     else:
#         defimg[:disp[0], :] = refimg[-disp[0]:, :]
#     if disp[1] >= 0:
#         defimg[:, disp[1]:] = defimg[:, :-disp[1]]
#     else:
#         defimg[:, :disp[1]] = defimg[:, -disp[1]:]
#     cv2.imwrite(filename=img[:-4]+"_DC.bmp", img=defimg)
#     cv2.imshow("Ref", refimg)
#     cv2.imshow("Def", defimg)
#     cv2.waitKey()
#
# if __name__=="__main__":
#     gendispcopy_img(img="D:/Research/Working-On/Tower_Disp_Monitor/Data/Image_20200403160132931.bmp", disp=[1, 1])

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def minmax_value(list1):
    minvalue = min(list1)
    maxvalue = max(list1)
    return minvalue, maxvalue


plt.figure(figsize=(16, 14), dpi=98)
xmajorLocator = MultipleLocator(1)  # 将x主刻度标签设置为1的倍数

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

p1 = plt.subplot(121)
p2 = plt.subplot(122)

# 图中展示点的数量
pointcount = 5

x = [i for i in range(20)]
print(x)

y1 = [i ** 2 for i in range(20)]
y2 = [i * 4 for i in range(20)]
y3 = [i * 3 + 2 for i in range(20)]
y4 = [i * 4 for i in range(20)]

for i in range(len(x) - 1):
    if i < pointcount:
        minx, maxx = minmax_value(x[:pointcount])
        minx, maxx = minmax_value(x[:pointcount])
        minyA, maxyA = minmax_value(y1[:pointcount])
        minyB, maxyB = minmax_value(y2[:pointcount])

        maxy1 = max(maxyA, maxyB)
        miny1 = min(minyA, minyB)
        p1.axis([minx, maxx, miny1, maxy1])
        p1.grid(True)
        A, = p1.plot(x[:pointcount], y1[:pointcount], "g-")
        B, = p1.plot(x[:pointcount], y2[:pointcount], "b-")

        # 设置主刻度标签的位置,标签文本的格式
        p1.xaxis.set_major_locator(xmajorLocator)
        legend = p1.legend(handles=[A, B], labels=["图1", "图2"])

        minx, maxx = minmax_value(x[:pointcount])
        minx, maxx = minmax_value(x[:pointcount])
        minyA, maxyA = minmax_value(y3[:pointcount])
        minyB, maxyB = minmax_value(y4[:pointcount])

        maxy1 = max(maxyA, maxyB)
        miny1 = min(minyA, minyB)
        p2.axis([minx, maxx, miny1, maxy1])
        p2.grid(True)
        A, = p2.plot(x[:pointcount], y3[:pointcount], "r-")
        B, = p2.plot(x[:pointcount], y4[:pointcount], "y-")

        # 设置主刻度标签的位置,标签文本的格式
        p2.xaxis.set_major_locator(xmajorLocator)
        legend = p2.legend(handles=[A, B], labels=["图3", "图4"])
    elif i >= pointcount:
        minx, maxx = minmax_value(x[i - pointcount:i])
        minx, maxx = minmax_value(x[i - pointcount:i])
        minyA, maxyA = minmax_value(y1[i - pointcount:i])
        minyB, maxyB = minmax_value(y2[i - pointcount:i])

        maxy1 = max(maxyA, maxyB)
        miny1 = min(minyA, minyB)
        p1.axis([minx, maxx, miny1, maxy1])
        p1.grid(True)
        A, = p1.plot(x[i - pointcount:i], y1[i - pointcount:i], "g-")
        B, = p1.plot(x[i - pointcount:i], y2[i - pointcount:i], "b-")

        # 设置主刻度标签的位置,标签文本的格式
        p1.xaxis.set_major_locator(xmajorLocator)
        legend = p1.legend(handles=[A, B], labels=["图1", "图2"])

        minx, maxx = minmax_value(x[i - pointcount:i])
        minx, maxx = minmax_value(x[i - pointcount:i])
        minyA, maxyA = minmax_value(y3[i - pointcount:i])
        minyB, maxyB = minmax_value(y4[i - pointcount:i])

        maxy1 = max(maxyA, maxyB)
        miny1 = min(minyA, minyB)
        p2.axis([minx, maxx, miny1, maxy1])
        p2.grid(True)
        A, = p2.plot(x[i - pointcount:i], y3[i - pointcount:i], "r-")
        B, = p2.plot(x[i - pointcount:i], y4[i - pointcount:i], "y-")

        # 设置主刻度标签的位置,标签文本的格式
        p2.xaxis.set_major_locator(xmajorLocator)
        legend = p2.legend(handles=[A, B], labels=["图3", "图4"])

    p1.set_xlabel("横轴属性名一", fontsize=14)
    p1.set_ylabel("纵轴属性名一", fontsize=14)
    p1.set_title("主题一", fontsize=18)

    p2.set_xlabel("横轴属性名二", fontsize=14)
    p2.set_ylabel("纵轴属性名二", fontsize=14)
    p2.set_title("主题二", fontsize=18)

    plt.pause(0.3)
    plt.tight_layout(pad=4, w_pad=4.0, h_pad=3.0)