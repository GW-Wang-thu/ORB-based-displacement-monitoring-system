import cv2
import numpy as np
from Matcher import ORB_matcher
from Ploter import Ploter
from Camera import GIGE_Camera
from Preprocess import Processor

import sys
import matplotlib.pylab as plt
sys.path.append("./MvImport")


class Monitor:

    def __init__(self, cameraid="0"):

        self.camera = GIGE_Camera(cameraid=cameraid)
        self.refimg = self.camera.getframe()
        self.defimg = self.camera.getframe()
        self.refpoints = []
        self._uploter = Ploter(num_wind=5, num_point=100)
        self._vploter = Ploter(num_wind=5, num_point=100)
        self._udisplist = []
        self._vdisplist = []
        self.__genshowimg__()
        self.__getpoints__()

    def __genshowimg__(self):
        img = np.column_stack((np.column_stack((self.refimg, (np.ones((3072, 14)) * 255).astype("uint8"))), self.defimg))
        self.showimg = cv2.resize(img, (1369, 1024), cv2.INTER_CUBIC)

    def __getpoints__(self):
        cv2.namedWindow('Select Points')
        while(1):
            # self.defimg = self.camera.read()
            self.__refreshdisp__(show=1)
            cv2.imshow("Select Points", self.tempshowimg)
            self._uploter.y = self._udisplist
            self._uploter.refresh()
            plt.pause(0.001)
            # self._vploter.y = self._vdisplist
            # self._vploter.refresh()
            cv2.setMouseCallback('Select Points', self.__selectpoint__)
            self.defimg = self.camera.getframe()
            self.__genshowimg__()
            if cv2.waitKey(10) == 27:
                print("Deselecting Points")
                cv2.setMouseCallback('Select Points', self.__Dselectpoint__)
                while not cv2.waitKey(10) & 0xFF == 27:
                    self.__refreshdisp__(show=1)
                    cv2.imshow("Select Points", self.tempshowimg)
                    self.defimg = self.camera.getframe()
                    self.__genshowimg__()
                    continue
                print("Selecting Points")
            # if cv2.waitKey(10) & 0xFF == 27:
            #     break

    def __selectpoint__(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            kp1, kp2, des1, matches, boxsize = self.__findkp__((x*3, y*3))
            if matches is not None:
                id1 = matches[0].queryIdx
                id2 = matches[0].trainIdx
                distance = matches[0].distance
                for i in range(len(matches)):
                    if matches[i].distance < distance:
                        distance = matches[i].distance
                        id1 = matches[i].queryIdx
                        id2 = matches[i].trainIdx
                des = np.zeros((1, des1.shape[1]))
                des[0, :] = des1[id1]
                self.refpoints.append([(x * 3 + (kp1[id1].pt[0] - boxsize), y * 3 + (kp1[id1].pt[1] - boxsize)), des, []])
                self._udisplist.append([0])
                self._vdisplist.append([0])

    def __Dselectpoint__(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            x_h = x * 3
            y_h = y * 3
            disp = 1e5
            min = None
            for i in range(len(self.refpoints)):
                if ((self.refpoints[i][0][0] - x_h)**2 + (self.refpoints[i][0][1] - y_h)**2) < disp:
                    min = i
            if len(self.refpoints) > 0 and min is not None:
                print(min)
                self.refpoints.pop(min)
                self._udisplist.pop(min)
                self._vdisplist.pop(min)

    def __findkp__(self, givenpoint):
        boxsize = 15
        refmatcher = ORB_matcher(nfeatures=30, scaleFactor=1.1, nlevels=5)      # 重要参数：推荐nfeature为tolerence的两倍
        defmatcher = ORB_matcher(nfeatures=30, scaleFactor=1.1, nlevels=5)
        while boxsize < 200:
            refbox = [(givenpoint[0]-boxsize, givenpoint[1]-boxsize), (givenpoint[0]+boxsize+1, givenpoint[1]+boxsize+1)]
            if any(refbox) < 0:
                break
            refblock = self.refimg[refbox[0][1]:refbox[1][1], refbox[0][0]:refbox[1][0]]
            kp1, des1 = refmatcher.detect(refblock, show=0)
            if des1 is not None:
                defbox = [(givenpoint[0]-boxsize-50, givenpoint[1]-boxsize-50), (givenpoint[0]+boxsize+51, givenpoint[1]+boxsize+51)]
                defblock = self.defimg[defbox[0][1]:defbox[1][1], defbox[0][0]:defbox[1][0]]
                if any(defbox) < 0:
                    print("out of range")
                    break
                kp2, des2 = defmatcher.detect(defblock, show=0)
                defmatcher.match(des1, des2)
                if len(defmatcher.matches) > 15:        # 重要参数：增大会增加匹配精度，但会减少匹配数量；根据特征点稀疏状况调整，特征点稀疏位置不方便使用太大
                    return kp1, kp2, des1, defmatcher.matches, boxsize
            boxsize += 5
        print("Key Point Not Found!")
        return None, None, None, None, None

    def __refreshdisp__(self, show):
        matcher = ORB_matcher(nfeatures=100, scaleFactor=1.2, nlevels=10)
        tempshowimg = self.showimg.copy()
        for i in range(len(self.refpoints)):
            defbox = [(int(self.refpoints[i][0][0]) - 200, int(self.refpoints[i][0][1]) - 200), (int(self.refpoints[i][0][0]) + 200, int(self.refpoints[i][0][1]) + 200)]
            defblock = self.defimg[defbox[0][1]:defbox[1][1], defbox[0][0]:defbox[1][0]]
            if any(defbox) < 0:
                print("out of range")
                break
            kp2, des2 = matcher.detect(defblock, show=0)
            des1 = self.refpoints[i][1].astype("uint8")
            matcher.match(des1, des2)
            if matcher.matches is not None:
                distance = matcher.matches[0].distance
                for j in range(len(matcher.matches)):
                    id2 = matcher.matches[0].trainIdx
                    if matcher.matches[j].distance < distance:
                        distance = matcher.matches[j].distance
                        id2 = matcher.matches[j].trainIdx
                x_ref = self.refpoints[i][0][0]
                y_ref = self.refpoints[i][0][1]
                x_def = kp2[id2].pt[0] - 200 + int(self.refpoints[i][0][0])
                y_def = kp2[id2].pt[1] - 200 + int(self.refpoints[i][0][1])
                u = x_def - x_ref
                v = y_def - y_ref
                self.refpoints[i][2] = [u, v]
                self._udisplist[i].append(u)
                self._vdisplist[i].append(u)
            else:
                self._udisplist[i].append(self._udisplist[i][-1])
                self._vdisplist[i].append(self._vdisplist[i][-1])

            cv2.circle(tempshowimg, (int(x_ref/3), int(y_ref/3)), 1, (255, 255, 255), 2)
            cv2.circle(tempshowimg, (int(x_def/3), int(y_def/3)), 1, (255, 255, 255), 2)

            if show:
                position1 = (int(self.refpoints[i][0][0]/3) + 5, int(self.refpoints[i][0][1]/3) - 10)
                position2 = (int(self.refpoints[i][0][0]/3) + 5, int(self.refpoints[i][0][1]/3) + 10)
                text1 = "U="+str(np.round(u, 3))
                text2 = "V="+str(np.round(v, 3))
                cv2.putText(tempshowimg, text1, position1,
                            fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(255, 255, 255), thickness=1)
                cv2.putText(tempshowimg, text2, position2,
                            fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(255, 255, 255), thickness=1)
        self.tempshowimg = tempshowimg

    # def show(self, savepath=None):
    #     if savepath:
    #         print("save markedimg to "+savepath)
    #         cv2.imwrite(savepath, savepath.markedref)
    #     cv2.imshow("MARKED REF IMG", cv2.resize(self.markedref, (720, 1080), cv2.INTER_CUBIC))
    #     cv2.waitKey()


if __name__=="__main__":
    # dir = "D:/Research/Working-On/Tower_Disp_Monitor/Data/"
    # outdir = "D:/Research/Working-On/Tower_Disp_Monitor/Data/out/"
    # # 读取图片内容
    # refimg = cv2.imread(dir + 'Image_20200403160132931.bmp', 0)
    # defimg = cv2.imread(dir + 'Image_20200403160130637.bmp', 0) # 04045
    # refimg = cv2.rotate(refimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # defimg = cv2.rotate(defimg, cv2.ROTATE_90_COUNTERCLOCKWISE)

    mymarker = Monitor(cameraid="0")

    # drawer = Plot(maxnum_window=2, num_point=100)
    # drawer.y = [[1, 1, 1, 2, 2], [1, 2, 1, 2, 1]]

