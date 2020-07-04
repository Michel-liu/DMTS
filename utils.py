import datetime
import time
import math
import random
from PIL import Image, ImageTk
import os


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
        self.logFileString = open(self.getCurTime()[:-7] + '_' + saveFilePath, 'w')

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

    def logMouseClick(self, x, y, regionIndex, addTrack=False, groundTrueRegion=None):
        theLogList = []
        nowTime = self.getCurTime(False)
        isCrorrect = None
        if addTrack:
            assert groundTrueRegion != None, "logMouseClick function needs the parm 'groundTrueRegion'!"
            if groundTrueRegion == regionIndex:
                isCrorrect = '1'
            else:
                isCrorrect = '0'
            self.mouseClickInfoList.append({
                "time": nowTime,
                "position": {
                    "x": x,
                    "y": y,
                    "region": regionIndex
                },
                "isCrorrect": int(isCrorrect),
                "distence": getDistence(index2XY(regionIndex), index2XY(groundTrueRegion))
            })
        theLogList.append(nowTime.__str__())
        theLogList.append(": Mouse Clicks ")
        theLogList.append(f"(x,y):({x},{y}), region: {regionIndex}")
        if addTrack:
            if int(isCrorrect) == 1:
                theLogList.append(", Correct")
                theLogList.append(f", Choose region: {regionIndex}")
                theLogList.append(f", Distance: {self.mouseClickInfoList[-1]['distence']}")

            else:
                theLogList.append(", Wrong")
                theLogList.append(f", Choose region: {regionIndex}")
                theLogList.append(f", Distance: {self.mouseClickInfoList[-1]['distence']}")
        self.list2LogFile(theLogList)

    def logSomething(self, content,addTime=True):
        """
        通用日志写入
        :param content:写入的内容 (无需包含时间信息)
        :return: 无
        """
        if addTime:
            theLogList = [self.getCurTime(), str(content)]
        else:
            theLogList = [str(content)]
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
            acc = len([x for x in self.keyPressInfoList if x['isCrorrect'] == 1]) / len(self.keyPressInfoList)
            self.logSomething(" :Acc: " + str(acc))
            return acc
        elif select == "mouse":
            assert len(self.mouseClickInfoList) == len(self.imgShowInfoList), "Tow list have different len"
            acc = len([x for x in self.mouseClickInfoList if x['isCrorrect'] == 1]) / len(self.mouseClickInfoList)
            distance = sum([x['distence'] for x in self.mouseClickInfoList]) / len(self.mouseClickInfoList)
            self.logSomething(": Acc: " + str(acc))
            self.logSomething(": Distance: " + str(distance))
            return acc

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
            avgTime = avgTime / len(self.imgShowInfoList)
            self.logSomething(" :AvgTime: " + str(avgTime))
            return avgTime
        else:
            assert len(self.mouseClickInfoList) == len(self.imgShowInfoList), "Tow list have different len"
            avgTime = None
            for i in range(len(self.imgShowInfoList)):
                if avgTime is not None:
                    avgTime = avgTime + (self.mouseClickInfoList[i]['time'] - self.imgShowInfoList[i]['time'])
                else:
                    avgTime = self.mouseClickInfoList[i]['time'] - self.imgShowInfoList[i]['time']
            avgTime = avgTime / len(self.imgShowInfoList)
            self.logSomething(": AvgTime: " + str(avgTime))
            return avgTime

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


img = None
photo = None


def loadPic(path, maxh, maxw):
    global img
    global photo
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
    x = x - (w - h) / 2
    if x < 0 or x > h:
        return -1
    mini_w = mini_h = round(h / yRegionCount)
    xIndex = math.floor(x / mini_w)
    yIndex = math.floor(y / mini_h)

    return yIndex * xRegionCount + xIndex


def createShowDataset(total_num=16, need_len=4):
    randInts = []
    lastInt = -1
    while True:
        currentInt = random.randint(0, total_num - 1)
        if currentInt != lastInt:
            randInts.append(currentInt)
            lastInt = currentInt
        if len(randInts) == need_len:
            break
    return randInts


def creatTestDataset(showList, total_num=16):
    """
    生成测试集随机序号列表,
    :param showList: 之前展示的图像序号 范围[0, 15], 共4个
    :return: 随机列表, 包含相同1张, 不同3张
    """
    showList_ = showList.copy()
    saveIndex = random.randint(0, len(showList_) - 1)
    for i in [x for x in range(4) if x != saveIndex]:
        leftChoices = [t for t in range(total_num) if t != showList_[i]]
        showList_[i] = random.choice(leftChoices)
    return showList_, saveIndex


class test4DatasetControl:
    def __init__(self, type_name=None):
        if type_name is None:
            type_name = ['green', 'red']
        self.type_name = type_name
        self.showPath = []
        self.testPath = []
        self.allPath = []
        self.mini_batch = None
        self.total_epoch = None
        self.rightIndex = []
        for name in type_name:
            for x in range(16):
                self.allPath.append(os.path.join(name, str(x) + '.png'))

    def isSameBetween(self):
        for i, item in enumerate(self.showPath[:-1]):
            if item == self.showPath[i+1]:
                return True
        return False

    def createTest4Dataset(self, epoch, mini_bach):
        total_num = epoch * mini_bach
        return createShowDataset(16, total_num)

    def createShowDataset(self, total_epoch, mini_bach):
        self.showPath = []
        assert total_epoch % len(self.type_name) == 0, "creatShowDataset % must be 0"
        self.mini_batch = mini_bach
        self.total_epoch = total_epoch
        for name in self.type_name:
            tList = self.createTest4Dataset(total_epoch // len(self.type_name), mini_bach)
            tList = list(map(lambda x: os.path.join(name, str(x) + '.png'), tList))
            self.showPath = self.showPath + tList
        assert len(self.showPath) % 4 == 0, "show list % 4 must be 0"
        random.shuffle(self.showPath)
        while self.isSameBetween():
            random.shuffle(self.showPath)

        return self.showPath

    def getShowDatasetByIndex(self, index):
        assert index <= self.total_epoch, "getShowDatasetByIndex: index must <= total_epoch"
        return self.showPath[
               index * (len(self.showPath) // self.total_epoch):(index + 1) * (len(self.showPath) // self.total_epoch)]

    def createTestDataset(self):
        self.testPath = []
        randIndexList = random.sample(range(len(self.showPath)), len(self.showPath)//4)
        for i in range(len(self.showPath)):
            if i in randIndexList:
                self.testPath.append(self.showPath[i])
                self.rightIndex.append(1)
            else:
                self.testPath.append(random.choice([x for x in self.allPath if x != self.showPath[i]]))
                self.rightIndex.append(-1)

    def getTestDatasetByIndex(self, index):
        assert index <= self.total_epoch, "getTestDatasetByIndex: index must <= total_epoch"
        rightList = []
        for i, num in enumerate(self.rightIndex[index*(len(self.testPath)//self.total_epoch):(index + 1) * (len(self.testPath)//self.total_epoch)]):
            if num == 1:
                rightList.append(i)

        return self.testPath[index*(len(self.testPath)//self.total_epoch):(index + 1) * (len(self.testPath)//self.total_epoch)], rightList

def getDistence(xy1, xy2):
    x1 = xy1[0]
    y1 = xy1[1]
    x2 = xy2[0]
    y2 = xy2[1]
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def index2XY(index):
    y = index // 4
    x = index - 4 * y
    return y, x

if __name__ == '__main__':
    # print(index2XY(15))
    # log = Logger()
    # log.logSomething("HHH",True)
    test = test4DatasetControl()
    test.createShowDataset(4, 4)
    print(test.getShowDatasetByIndex(0))
    print(test.getShowDatasetByIndex(1))
    test.createTestDataset()
    print(test.getTestDatasetByIndex(0))
    print(test.getTestDatasetByIndex(1))
