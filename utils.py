import datetime
import time
class Logger:
    def __init__(self, saveFilePath='log.txt', name='test1'):
        self.imgShowInfoList = []
        self.keyPressInfoList = []

        with open(saveFilePath, 'w') as f:
            self.logFileString = f

    def logImgShow(self, theImg, addTrack=False):
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

    def logPressKey(self, theKey, addTrack=False, isCrorrect=''):
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

    def logSomething(self, content):
        theLogList = [str(content)]


    def getTestAcc(self):
        assert len(self.keyPressInfoList) == len(self.imgShowInfoList), "Tow list have different len"
        return len([x for x in self.imgShowInfoList if x['isCrorrect'] == 1])/len(self.imgShowInfoList)



    def list2LogFile(self, logList, endWith='\n'):
        if len(logList) == 0:
            return
        for i in logList:
            self.logFileString.write(i)
        self.logFileString.write(endWith)

    def getCurTime(self, str=True):
        if str:
            return datetime.datetime.now().__str__()
        else:
            return datetime.datetime.now()

if __name__ == '__main__':
    # time_now = datetime.datetime.now()
    print(datetime.datetime.now().__str__())
    # time.sleep(1)
    # time_now_1 = datetime.datetime.now().strftime('%H:%M:%S.%f')

