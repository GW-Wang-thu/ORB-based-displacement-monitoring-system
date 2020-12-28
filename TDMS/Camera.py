from MvImport import *
from MvImport.MvCameraControl_class import *
import sys
sys.path.append("./MvImport")

class GIGE_Camera:

    def __init__(self, cameraid="0"):
        # ch:创建相机实例 | en:Creat Camera Object
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE, self.deviceList)
        if ret != 0:
            print("enum devices fail! ret[0x%x]" % ret)
            sys.exit()
        # # ch:选择设备并创建句柄 | en:Select device and create handle
        self.cam = MvCamera()
        self.stDeviceList = cast(self.deviceList.pDeviceInfo[int(cameraid)], POINTER(MV_CC_DEVICE_INFO)).contents
        ret = self.cam.MV_CC_CreateHandle(self.stDeviceList)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)
            sys.exit()
        # ch:打开设备 | en:Open device
        ret = self.cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print("open device fail! ret[0x%x]" % ret)
            sys.exit()
        # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if self.stDeviceList.nTLayerType == MV_GIGE_DEVICE:
            self.nPacketSize = self.cam.MV_CC_GetOptimalPacketSize()
            if int(self.nPacketSize) > 0:
                ret = self.cam.MV_CC_SetIntValue("GevSCPSPacketSize", self.nPacketSize)
                # if ret != 0:
                #     print("Warning: Set Packet Size fail! ret[0x%x]" % ret)
            else:
                print("Warning: Get Packet Size fail! ret[0x%x]" % self.nPacketSize)
        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = self.cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print("set trigger mode fail! ret[0x%x]" % ret)
            sys.exit()
        # ch:获取数据包大小 | en:Get payload size
        self.stParam = MVCC_INTVALUE()
        memset(byref(self.stParam), 0, sizeof(MVCC_INTVALUE))
        self.ret = self.cam.MV_CC_GetIntValue("PayloadSize", self.stParam)
        if ret != 0:
            print("get payload size fail! ret[0x%x]" % ret)
            sys.exit()
        self.nPayloadSize = self.stParam.nCurValue
        ret = self.cam.MV_CC_StartGrabbing()
        i = 0
        while ret != 0:
            ret = self.cam.MV_CC_StartGrabbing()
            i += 1
            if i > 10:
                print("start grabbing fail! ret[0x%x]" % ret)
                sys.exit()
        timg = self.getframe()

    def getframe(self, rot=1):

        # ch:开始取流 | en:Start grab image
        self.stDeviceList = MV_FRAME_OUT_INFO_EX()
        memset(byref(self.stDeviceList), 0, sizeof(self.stDeviceList))
        data_buf = (c_ubyte * self.nPayloadSize)()

        ret = self.cam.MV_CC_GetOneFrameTimeout(byref(data_buf), self.nPayloadSize, self.stDeviceList, 1000)
        if ret == 0:
            print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (
            self.stDeviceList.nWidth, self.stDeviceList.nHeight, self.stDeviceList.nFrameNum))
            array = np.ctypeslib.as_array(data_buf)
            array = array.reshape(2048, 3072)
            if rot:
                array = cv2.rotate(array, cv2.ROTATE_90_COUNTERCLOCKWISE)
            return array
        else:
            return 0

