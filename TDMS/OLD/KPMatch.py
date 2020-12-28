import cv2
from OLD.marker import Marker


def main():
    dir = "D:/Research/Working-On/Tower_Disp_Monitor/Data/"
    outdir = "D:/Research/Working-On/Tower_Disp_Monitor/Data/out/"
    # 读取图片内容
    refimg = cv2.imread(dir + 'Image_20200403154001602.bmp', 0)
    defimg = cv2.imread(dir + 'Image_20200403154004045.bmp', 0)
    refimg = cv2.rotate(refimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    defimg = cv2.rotate(defimg, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # refimg = preprocess(refimg)
    # defimg = preprocess(defimg)

    marker = Marker(refimg, defimg, blocksize=50, pointlist=[(1020, 500), (1020, 700), (1020, 900), (1020, 1100), (1000, 1300)])
    marker.Disp(show=1)

    # machedimg = outdir + "Image_matched-2.bmp"
    # matcher = ORB_matcher(nfeatures=1000, scaleFactor=1.2, nlevels=10)
    #
    # kp1, des1 = matcher.detect(refimg, show=1)
    # kp2, des2 = matcher.detect(defimg, show=1)
    # matcher.match(des1, des2)
    # U, V = matcher.CalculateDisp(kp1, kp2, refimg, defimg)
    # matcher.show()
    # matcher.save(machedimg)

if __name__ == "__main__":
    main()