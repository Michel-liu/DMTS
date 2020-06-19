import datetime
import time
class Logger:
    def __init__(self, saveFilePath='log.txt', name='test1'):
        self.imgShowTimeList = []
        self.keyPressTimeList = []

        with open(saveFilePath, 'w') as f:
            self.logFileString = f

    def logPressKey(self, theKey):
        theLogList = []
        theLogList.append(self.getCurTime())
        theLogList.append(": Press Button ")
        theLogList.append(str(theKey))

        theLogList.append('\n')

    def getCurTime(self):
        return datetime.datetime.now().__str__()

if __name__ == '__main__':
    # time_now = datetime.datetime.now()
    print(datetime.datetime.now().__str__())
    # time.sleep(1)
    # time_now_1 = datetime.datetime.now().strftime('%H:%M:%S.%f')

