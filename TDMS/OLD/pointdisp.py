import cv2
import numpy as np
from Matcher import ORB_matcher

class Pointmarker:

    def __init__(self, refimg, defimg, cameraid=0):
        self.refimg = refimg
        self.defimg = defimg
        # self.camera = cv2.VideoCapture(cameraid)
        self.refpoints = []
        self.__genshowimg__()
        self.__getpoints__()


    def __genshowimg__(self):
        img = np.column_stack((np.column_stack((self.refimg, (np.ones((3072, 14)) * 255).astype("uint8"))), self.defimg))
        self.showimg = cv2.resize(img, (1369, 1024), cv2.INTER_CUBIC)

    def __getpoints__(self):
        cv2.namedWindow('Select Points')
        cv2.setMouseCallback('Select Points', self.__selectpoint__)
        while(1):
            # self.defimg = self.camera.read()
            self.__refreshdisp__(show=1)
            cv2.imshow("Select Points", self.showimg)
            if cv2.waitKey(20) & 0xFF == 27:
                break

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
                cv2.circle(self.showimg, (x + int((kp1[id1].pt[0] - boxsize)/3), y + int((kp1[id1].pt[1] - boxsize)/3)), 1, (255, 255, 255), 2)
                cv2.circle(self.showimg, (x + int((kp2[id2].pt[0] + 2062 - boxsize - 50)/3), y + int((kp2[id2].pt[1] - boxsize - 50)/3)), 1, (255, 255, 255), 2)

    def __findkp__(self, givenpoint):
        boxsize = 15
        refmatcher = ORB_matcher(nfeatures=20, scaleFactor=1.1, nlevels=5)      # 重要参数：推荐nfeature为tolerence的两倍
        defmatcher = ORB_matcher(nfeatures=20, scaleFactor=1.1, nlevels=5)
        while boxsize < 100:
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
                if len(defmatcher.matches) > 10:        # 重要参数：增大会增加匹配精度，但会减少匹配数量；根据特征点稀疏状况调整，特征点稀疏位置不方便使用太大
                    return kp1, kp2, des1, defmatcher.matches, boxsize
            boxsize += 5
        print("Key Point Not Found!")
        return None, None, None, None, None

    def __refreshdisp__(self, show):
        matcher = ORB_matcher(nfeatures=100, scaleFactor=1.2, nlevels=10)
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
            if show:
                position1 = (int(self.refpoints[i][0][0]/3) + 5, int(self.refpoints[i][0][1]/3) - 10)
                position2 = (int(self.refpoints[i][0][0]/3) + 5, int(self.refpoints[i][0][1]/3) + 10)
                text1 = "U="+str(np.round(u, 3))
                text2 = "V="+str(np.round(v, 3))
                cv2.putText(self.showimg, text1, position1,
                            fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(255, 255, 255), thickness=1)
                cv2.putText(self.showimg, text2, position2,
                            fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(255, 255, 255), thickness=1)

    # def show(self, savepath=None):
    #     if savepath:
    #         print("save markedimg to "+savepath)
    #         cv2.imwrite(savepath, savepath.markedref)
    #     cv2.imshow("MARKED REF IMG", cv2.resize(self.markedref, (720, 1080), cv2.INTER_CUBIC))
    #     cv2.waitKey()
if __name__=="__main__":
    dir = "D:/Research/Working-On/Tower_Disp_Monitor/Data/"
    outdir = "D:/Research/Working-On/Tower_Disp_Monitor/Data/out/"
    # 读取图片内容
    refimg = cv2.imread(dir + 'Image_20200403160132931.bmp', 0)
    defimg = cv2.imread(dir + 'Image_20200403160130637.bmp', 0) # 04045
    refimg = cv2.rotate(refimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    defimg = cv2.rotate(defimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    mymarker = Pointmarker(refimg, defimg)
