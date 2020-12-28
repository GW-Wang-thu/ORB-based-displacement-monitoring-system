import cv2
import numpy as np
import torch
from utils import VDSR, RealSR


class Processor:

    def __init__(self, imsize=(3072, 2048)):
        self.imsize = imsize

    def denoise(self, img, method="Gaussian", ksize=3):
        if method == "Gaussian":
            out_img = cv2.GaussianBlur(img, ksize)
        if method == "Median":
            out_img = cv2.medianBlur(img, ksize)
        if method == "Bilater":
            out_img = cv2.bilateralFilter(img, ksize, 31, 31)

    def enhance(self, img, crop=(0, 0), methpd="Linear"):
        out = img * img > crop[0]
        out = (out - 255) * (out < crop[1]) + 255

        if methpd == "Linear":
            scale = (np.max(out) - np.min(out))
            out = out * 255 / scale

        if methpd == "Regular":
            out = cv2.normalize(out, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)

        out = out.astype("uint8")
        return out

    def deblure(self, img, method="VDSR"):
        if method == "VDSR":
            model = VDSR.model()
            model.load_state_dict("./utils/vdsrparams.pth")
            out = model(img)
            out = model.post(out)
        if method == "RealSR":
            model = RealSR.model()
            model.load_state_dict("./utils/realsrparams.pth")
            out = model(img)
            out = model.post(out)
        return out

    def sharpen(self, img, ksize=3):
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], np.float32)  # 定义一个核
        out = cv2.filter2D(img, -1, kernel=kernel)
        return out

    def Sequencial_process(self, img, operations):
        for i in range(len(operations)):
            out = exec("self."+operations[i][0]+"(img, "+operations[i][1]+")")
        return out