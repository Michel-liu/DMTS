import datetime
import time
import math
import random
from PIL import Image, ImageTk


class Logger:
    """ 日志记录类
    负责向指定的文件路径中写入运行日志
    """

    def __init__(self, saveFilePath='log.txt', name='test1'):
        """
        初始化
        :param saveFilePath: 写入日志文件的路径 *必须指定
        :param name: 测试用户的相关信息, 供后续拓展
        """
        self.imgShowInfoList = []
        self.keyPressInfoList = []
        self.mouseClickInfoList = []

        self.logFileString = open(saveFilePath, 'w')

    def logImgShow(self, theImg, addTrack=False):
        """
        记录图像展示
        :param theImg: 图像的编号或名字 可传入str或int
        :param addTrack: 是否添加追踪 在最后测试用户反应阶段的图像, 需指定为True以记录反应时间
        :return:无
        """
        theLogList = []
        nowTime = self.getCurTime(False)
        if addTrack:
            self.imgShowInfoList.append({
                "time": nowTime,
                "img": theImg
            })
        theLogList.append(nowTime.__str__())
        theLogList.append(": Show Img ")
        theLogList.append(str(theImg))
        self.list2LogFile(theLogList)

    def logPressKey(self, theKey, addTrack=False, isCrorrect=''):
        """
        记录键盘点击事件
        :param theKey: 点按键盘按键的编号或名字 可传入str或int
        :param addTrack: 是否添加追踪 在最后测试用户反应阶段，需指定为True以记录反应时间
        :param isCrorrect: 按键判断情况 正确为'1' 错误为'0' 可传入str或int, 在addTrack为True时需指定，供计算正确率
        :return:无
        """
        theLogList = []
        nowTime = self.getCurTime(False)
        if addTrack:
            assert isCrorrect != '', "logPressKey function needs the parm 'isCrorrect'!"
            self.keyPressInfoList.append({
                "time": nowTime,
                "key": theKey,
                "isCrorrect": int(isCrorrect)
            })
        theLogList.append(nowTime.__str__())
        theLogList.append(": Press Button ")
        theLogList.append(str(theKey))
        if addTrack:
            if int(isCrorrect) == 1:
                theLogList.append(", Correct")
            else:
                theLogList.append(", Wrong")
        self.list2LogFile(theLogList)

    def logMouseClick(self, x, y, regionIndex, addTrack=False, isCrorrect=''):
        theLogList = []
        nowTime = self.getCurTime(False)
        if addTrack:
            assert isCrorrect != '', "logMouseClick function needs the parm 'isCrorrect'!"
            self.mouseClickInfoList.append({
                "time": nowTime,
                "position": {
                    "x": x,
                    "y": y,
                    "region": regionIndex
                },
                "isCrorrect": int(isCrorrect)
            })
        theLogList.append(nowTime.__str__())
        theLogList.append(": Mouse Clicks ")
        theLogList.append(f"(x,y):({x},{y}), region: {regionIndex}")
        if addTrack:
            if int(isCrorrect) == 1:
                theLogList.append(", Correct")
            else:
                theLogList.append(", Wrong")
        self.list2LogFile(theLogList)

    def logSomething(self, content):
        """
        通用日志写入
        :param content:写入的内容 (无需包含时间信息)
        :return: 无
        """
        theLogList = [self.getCurTime(), str(content)]
        self.list2LogFile(theLogList)

    def getTestAcc(self, select):
        """
        计算测试正确率
        :param select: 计算哪种类型的正确率 str: "key" or "mouse"
        :return: 正确率 float
        """
        assert select == "key" or select == "mouse", "getTestAcc function need parm select"
        if select == "key":
            assert len(self.keyPressInfoList) == len(self.imgShowInfoList), "Tow list have different len"
            return len([x for x in self.keyPressInfoList if x['isCrorrect'] == 1]) / len(self.keyPressInfoList)
        elif select == "mouse":
            assert len(self.mouseClickInfoList) == len(self.imgShowInfoList), "Tow list have different len"
            return len([x for x in self.mouseClickInfoList if x['isCrorrect'] == 1]) / len(self.mouseClickInfoList)

    def getAvgActTime(self, select):
        """
        计算测试平均反应时间
        :param select: 计算哪种类型的正确率 str: "key" or "mouse"
        :return: 平均反应时间 datetime.datetime
        """
        assert select == "key" or select == "mouse", "getAvgActTime function need parm select"
        if select == "key":
            assert len(self.keyPressInfoList) == len(self.imgShowInfoList), "Tow list have different len"
            avgTime = None
            for i in range(len(self.imgShowInfoList)):
                if avgTime is not None:
                    avgTime = avgTime + (self.keyPressInfoList[i]['time'] - self.imgShowInfoList[i]['time'])
                else:
                    avgTime = self.keyPressInfoList[i]['time'] - self.imgShowInfoList[i]['time']
            return avgTime / len(self.imgShowInfoList)
        else:
            assert len(self.mouseClickInfoList) == len(self.imgShowInfoList), "Tow list have different len"
            avgTime = None
            for i in range(len(self.imgShowInfoList)):
                if avgTime is not None:
                    avgTime = avgTime + (self.mouseClickInfoList[i]['time'] - self.imgShowInfoList[i]['time'])
                else:
                    avgTime = self.mouseClickInfoList[i]['time'] - self.imgShowInfoList[i]['time']
            return avgTime / len(self.imgShowInfoList)

    def list2LogFile(self, logList, endWith='\n'):
        """
        传入列表写入
        :param logList: 待写入内容列表
        :param endWith: 写入内容的结束符 默认回车
        :return: 无
        """
        if len(logList) == 0:
            return
        for i in logList:
            self.logFileString.write(i)
        self.logFileString.write(endWith)

    def getCurTime(self, str=True):
        """
        获取当前时间
        :param str: 是否需要转换为str格式返回 默认True
        :return: 当前时间 str或datetime.datetime
        """
        if str:
            return datetime.datetime.now().__str__()
        else:
            return datetime.datetime.now()

    def closeFile(self):
        """
        关闭日志文件
        :return: 无
        """
        self.logFileString.close()


def handlerAdaptor(fun, **kwds):
    """
    用于给函数作为参数时传参是使用
    :param fun: 函数对象
    :param kwds: 函数的参数
    :return 无
    """
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


def callback(event):
    """
    处理鼠标左键点击事件
    :param maxw:图像宽度
    :param path:图像高度
    :param event:鼠标点击事件对象
    :return:无
    """
    print(event.char)

    return event.char


def callbackStart(event, maxw, maxh):
    """

    :param event:
    :return:
    """
    photo = loadPic(r'./img/1_16.png', maxw, maxh)
    label = event.widget
    label.configure(image=photo)
    # 十字显示500ms
    time.sleep(0.5)
    # 随机显示四个图片
    photo = loadPic(r'./img/5.png', maxw, maxh)
    label.configure(image=photo)
    time.sleep(1)

    photo = loadPic(r'./img/9.png', maxw, maxh)
    label.configure(image=photo)
    time.sleep(1)

    photo = loadPic(r'./img/13.png', maxw, maxh)
    label.configure(image=photo)
    time.sleep(1)

    photo = loadPic(r'./img/2.png', maxw, maxh)
    label.configure(image=photo)
    time.sleep(1)


def resize(w, h, w_box, h_box, pil_image):
    '''
  resize a pil_image object so it will fit into
  a box of size w_box times h_box, but retain aspect ratio
  对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
  '''
    f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


def loadPic(path, maxh, maxw):
    img = Image.open(path)
    w, h = img.size
    img_resize = resize(h, w, maxh, maxw, img)
    photo = ImageTk.PhotoImage(img_resize)
    return photo


def whereIAm(h, w, x, y, xRegionCount=4, yRegionCount=4):
    """
    点击位置判断函数
    :param h:窗口高度
    :param w:窗口宽度
    :param x: 鼠标点击 x坐标
    :param y: 鼠标点击 y坐标
    :param xRegionCount: 区域横向被均分的个数 默认4
    :param yRegionCount: 区域纵向被均分的个数 默认4
    :return: 区域编码 范围 0 - (xRegionCount * yRegionCount - 1) 由左至右, 由上到下
    """
    assert x <= w and y <= h, "超出区域限制范围, 检查输入"
    mini_h = round(h / yRegionCount)
    mini_w = round(w / xRegionCount)

    xIndex = math.floor(x / mini_w)
    yIndex = math.floor(y / mini_h)

    return yIndex * xRegionCount + xIndex



# if __name__ == '__main__':
def creatTestDataset(showList):
    """
    生成测试集随机序号列表,
    :param showList: 之前展示的图像序号 范围[0, 15], 共4个
    :return: 随机列表, 包含相同1张, 不同3张
    """
    saveIndex = random.randint(0, len(showList)-1)
    for i in [x for x in range(4) if x != saveIndex]:
        leftChoices = [t for t in range(16) if t != showList[i]]
        showList[i] = random.choice(leftChoices)
    return showList,saveIndex


# if __name__ == '__main__':
# logger = Logger()
    # logger.logImgShow(1, True)
    # time.sleep(0.5)
    # logger.logPressKey('m', True, '1')
    # time.sleep(1)
    # logger.logImgShow(2, True)
    # time.sleep(0.5)
    # logger.logPressKey('c', True, '0')
    # logger.closeFile()
    # print(logger.getTestAcc())
    # print(logger.getAvgActTime())
    # print(whereIAm(100, 100, 99, 99))
