import cv2
import numpy as np
from Matcher import ORB_matcher


class Marker:

    def __init__(self, refimg, defimg, pointlist, blocksize=100, matcher=ORB_matcher(nfeatures=100, scaleFactor=1.2, nlevels=10)):
        '''
        :param refimg: Reference image, class 2D array,
        :param defimg: Deformed image of the same size of reference image
        :param pointlist: Concerning region center points list, class tuple
        :param blocksize: Patch size of detecting area around given point in reference image, an EVEN number needed
                        For example: A point(100, 200) with blocksize(100) will leading to a calculation area
                        of [50:150, 150:250]
        :param matcher: A matcher must be given to match kps and get point-positions of the two images
        '''
        self.refimg = refimg
        self.defimg = defimg
        self.markedref = refimg.copy()
        self.pointlist = pointlist
        self.blocksize = blocksize
        self.matcher = matcher
        self.__CalculatePatchDisp__()
        self.__genmarkedimg__()


    def __CalculatePatchDisp__(self):
        self.PatchDisp = []
        temrefblock = np.zeros((self.blocksize+100+1, self.blocksize+100+1)).astype("uint8")
        Enlargerefimg = np.zeros((self.refimg.shape[0]+self.blocksize, self.refimg.shape[1]+self.blocksize))
        Enlargerefimg[self.blocksize//2:-self.blocksize//2, self.blocksize//2:-self.blocksize//2] = self.refimg
        Enlargedefimg = np.zeros((self.refimg.shape[0]+self.blocksize+100, self.refimg.shape[1]+self.blocksize+100))
        Enlargedefimg[(self.blocksize+100)//2:-(self.blocksize+100)//2, (self.blocksize+100)//2:-(self.blocksize+100)//2] = self.refimg
        for i in range(len(self.pointlist)):
            temrefblock[50:-50, 50:-50] = self.refimg[(self.pointlist[i][0]-self.blocksize//2):(self.pointlist[i][0]+self.blocksize//2)+1,
                                                      (self.pointlist[i][1]-self.blocksize//2):(self.pointlist[i][1]+self.blocksize//2)+1]
            temdefblock = self.defimg[(self.pointlist[i][0]-self.blocksize//2-50):(self.pointlist[i][0]+self.blocksize//2+50+1),
                                      (self.pointlist[i][1]-self.blocksize//2-50):(self.pointlist[i][1]+self.blocksize//2+50+1)]
            kp1, des1 = self.matcher.detect(temrefblock, show=0)
            kp2, des2 = self.matcher.detect(temdefblock, show=0)
            if (des1 is None) or (des2 is None):
                print("Warning: No matched points in the block around {}".format(self.pointlist[i]))
                continue
            self.matcher.match(des1, des2)
            block_U, block_V = self.matcher.CalculateDisp(kp1, kp2, temrefblock, temdefblock)
            U, V = self.__meanUV__(block_U, block_V)
            self.PatchDisp.append([self.pointlist[i], (U, V)])

    def __meanUV__(self, block_U, block_V):
        maxu, minu = np.max(block_U), np.min(block_U)
        maxv, minv = np.max(block_V), np.min(block_V)
        if abs(maxu)>=abs(minu):
            U=maxu
        else:
            U=minu
        if abs(maxv) >= abs(minv):
            V = maxv
        else:
            V = minv
        return U, V

    def __genmarkedimg__(self):

        if not len(self.PatchDisp):
            print("Warning: No Displacement Calculated")
        img = self.markedref
        for i in range(len(self.PatchDisp)):
            cv2.circle(img=img,
                       center=self.PatchDisp[i][0],
                       radius=4, color=(255, 255, 255), lineType=0, thickness=5)
            cv2.putText(img=img,
                        text="Disp: "+str(self.PatchDisp[i][1]),
                        org=(self.PatchDisp[i][0][0]+50, self.PatchDisp[i][0][1]+50),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)


    def Disp(self, show=0, savepath=None):
        if savepath:
            cv2.imwrite(savepath, savepath.markedref)
        if show:
            cv2.imshow("MARKED REF IMG", cv2.resize(self.markedref, (720, 1080), cv2.INTER_CUBIC))
            cv2.waitKey()
