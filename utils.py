import datetime
import time

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

    def logSomething(self, content):
        """
        通用日志写入
        :param content:写入的内容 (无需包含时间信息)
        :return: 无
        """
        theLogList = [self.getCurTime(), str(content)]
        self.list2LogFile(theLogList)

    def getTestAcc(self):
        """
        计算测试正确率
        :return: 正确率 float
        """
        assert len(self.keyPressInfoList) == len(self.imgShowInfoList), "Tow list have different len"
        return len([x for x in self.keyPressInfoList if x['isCrorrect'] == 1])/len(self.keyPressInfoList)

    def getAvgActTime(self):
        """
        计算测试平均反应时间
        :return: 平均反应时间 datetime.datetime
        """
        assert len(self.keyPressInfoList) == len(self.imgShowInfoList), "Tow list have different len"
        avgTime = None
        for i in range(len(self.imgShowInfoList)):
            if avgTime is not None:
                avgTime = avgTime + (self.keyPressInfoList[i]['time'] - self.imgShowInfoList[i]['time'])
            else:
                avgTime = self.keyPressInfoList[i]['time'] - self.imgShowInfoList[i]['time']
        return avgTime/len(self.imgShowInfoList)

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


if __name__ == '__main__':
    logger = Logger()
    logger.logImgShow(1,True)
    time.sleep(0.5)
    logger.logPressKey('m', True, '1')
    time.sleep(1)
    logger.logImgShow(2,True)
    time.sleep(0.5)
    logger.logPressKey('c', True, '0')
    logger.closeFile()
    print(logger.getTestAcc())
    print(logger.getAvgActTime())