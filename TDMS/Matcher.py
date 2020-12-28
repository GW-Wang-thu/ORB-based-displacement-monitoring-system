import cv2
import numpy as np


class ORB_matcher:
    def __init__(self, nfeatures=1000, scaleFactor=1.2, nlevels=8):
        self.orb = cv2.ORB_create(nfeatures=nfeatures,
                                  scaleFactor=scaleFactor,
                                  nlevels=nlevels)
        self.matcher = cv2.BFMatcher(normType=cv2.NORM_HAMMING,
                                     crossCheck=True)

    def detect(self, img_0, show=0, draw_marker_in_result=1):
        if not draw_marker_in_result:
            img = img_0.copy()
        else:
            img = img_0
        kp, des = self.orb.detectAndCompute(img, None)
        # print("Num of KPs: ", len(kp))
        if show:
            for i in range(len(kp)):
                img = cv2.circle(img=img,
                                 center=(int(kp[i].pt[0]), int(kp[i].pt[1])),
                                 radius=4, color=(255, 255, 255), lineType=0, thickness=5)
            # img = cv2.resize(img, (720, 1080), cv2.INTER_CUBIC)
            cv2.imshow("Detected Image", img)
            cv2.waitKey()
        return kp, des

    def match(self, des1, des2):
        matches = self.matcher.match(des1, des2)
        self.matches = sorted(matches, key=lambda x: x.distance)
        # print("Num of matches: ", len(matches))

    def CalculateDisp(self, kp1, kp2, refimg, defimg):
        U_displacement = np.zeros_like(refimg)
        V_displacement = np.zeros_like(refimg)
        for i in range(len(self.matches)):
            idx1 = self.matches[i].queryIdx
            idx2 = self.matches[i].trainIdx
            location = np.array([kp1[idx1].pt[0], kp1[idx1].pt[1]], dtype="int")
            disp = np.array([kp2[idx2].pt[0], kp2[idx2].pt[1]]) - np.array([kp1[idx1].pt[0], kp1[idx1].pt[1]])
            U_displacement[location[1], location[0]] = disp[0]
            V_displacement[location[1], location[0]] = disp[1]
            # print("point (%d, %d) in reference image has a displacement of " % (kp1[idx1].pt[0], kp1[idx1].pt[1]), disp)
            self.matchedimg = cv2.drawMatches(img1=refimg, keypoints1=kp1, img2=defimg, keypoints2=kp2,
                                              matches1to2=self.matches, outImg=defimg, flags=2)
        return U_displacement, V_displacement

    def show(self):
        img = cv2.resize(self.matchedimg, (1920, 1080), cv2.INTER_CUBIC)
        cv2.imshow("Detected img", img)
        if cv2.waitKey():
            cv2.destroyAllWindows()

    def save(self, fname):
        cv2.imwrite(fname, self.matchedimg)