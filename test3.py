# 延迟回忆-位置

from tkinter import *
from tkinter import messagebox

import config
from utils import *
import random

PRACTICE = 0
REALTEST = 1


class mainProcess:
    def __init__(self):
        self.showScreen = [Toplevel(), Toplevel()]
        for o in self.showScreen:
            o.withdraw()
        self.controlVal = [{'value': 0, 'IntVar': IntVar(self.showScreen[PRACTICE], 0, name="PRACTICE"), 'state': 0},
                           {'value': 0, 'IntVar': IntVar(self.showScreen[REALTEST], 0, name="REALTEST"), 'state': 0}]
        self.SCREEN_WIDTH = self.showScreen[PRACTICE].winfo_screenwidth()
        self.SCREEN_HEIGHT = self.showScreen[PRACTICE].winfo_screenheight()
        self.CURRENTTRUE = False
        self.CURRENTINDEX = -1
        self.USETCHOICE = -1
        self.logger = Logger(saveFilePath="test3.log")
        self.LOCK = None

    def destroy(self, choice):
        self.showScreen[choice].destroy()
        self.showScreen[choice] = Toplevel()
        self.showScreen[choice].withdraw()
        self.controlVal[choice]['state'] = 0
        if choice == PRACTICE:
            self.controlVal[choice]['IntVar'] = IntVar(self.showScreen[choice], 0, name="PRACTICE")
        else:
            self.controlVal[choice]['IntVar'] = IntVar(self.showScreen[choice], 0, name="REALTEST")
        self.controlVal[choice]['value'] = 0

    def waitPracticeClick(self, event):
        # 等待鼠标点击
        if event.type == "2":
            if event.char == ' ' and self.controlVal[PRACTICE]['state'] == 0:
                # self.controlVal[PRACTICE]['state'] = 1
                self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[PRACTICE], 1, name="PRACTICE")
                self.controlVal[PRACTICE]['value'] = 1
        if event.type == "4" and self.controlVal[PRACTICE]['state'] == 1 and self.LOCK == False:
            self.LOCK = True
            print("CLick in")
            self.USETCHOICE = whereIAm(self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_WIDTH, event.x, event.y)
            if self.USETCHOICE < 0:
                return
            print(self.USETCHOICE)

            if self.controlVal[PRACTICE]['value'] == 0:
                self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[REALTEST], 1, name="PRACTICE")
                self.controlVal[PRACTICE]['value'] = 1
            elif self.controlVal[PRACTICE]['value'] == 1:
                self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[REALTEST], 0, name="PRACTICE")
                self.controlVal[PRACTICE]['value'] = 0

            if self.USETCHOICE == self.CURRENTINDEX:
                print("正确！")
                # self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='1')
                self.logger.logMouseClick(event.x, event.y, self.USETCHOICE, addTrack=TRUE,
                                          groundTrueRegion=self.CURRENTINDEX)
            else:
                print("错误！")
                # self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='0')
                self.logger.logMouseClick(event.x, event.y, self.USETCHOICE, addTrack=TRUE,
                                          groundTrueRegion=self.CURRENTINDEX)

    def waitRealTestClick(self, event):
        # 等待鼠标点击
        if event.type == "2":
            if event.char == ' ' and self.controlVal[REALTEST]['state'] == 0:
                # self.controlVal[PRACTICE]['state'] = 1
                self.controlVal[REALTEST]['IntVar'] = IntVar(self.showScreen[REALTEST], 1, name="REALTEST")
                self.controlVal[REALTEST]['value'] = 1
        if event.type == "4" and self.controlVal[REALTEST]['state'] == 1 and self.LOCK == False:
            self.LOCK = True
            print("wait realtest button1 CLick in")
            self.USETCHOICE = whereIAm(self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_WIDTH, event.x, event.y)
            if self.USETCHOICE < 0:
                return
            print(self.USETCHOICE)
            if self.controlVal[REALTEST]['value'] == 0:
                self.controlVal[REALTEST]['IntVar'] = IntVar(self.showScreen[REALTEST], 1, name="REALTEST")
                self.controlVal[REALTEST]['value'] = 1
            elif self.controlVal[REALTEST]['value'] == 1:
                self.controlVal[REALTEST]['IntVar'] = IntVar(self.showScreen[REALTEST], 0, name="REALTEST")
                self.controlVal[REALTEST]['value'] = 0
            if self.USETCHOICE == self.CURRENTINDEX:
                print("正确！")
                # self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='1')
                self.logger.logMouseClick(event.x, event.y, self.USETCHOICE, addTrack=TRUE, groundTrueRegion=self.CURRENTINDEX)
            else:
                print("错误！")
                # self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='0')
                self.logger.logMouseClick(event.x, event.y, self.USETCHOICE, addTrack=TRUE, groundTrueRegion=self.CURRENTINDEX)

    def canvasChangePic(self, imHandler, imgPath, imgWidth, imgHeight, sleepTime, choice, theCanvas):
        theCanvas = theCanvas[0]
        photo = loadPic(imgPath, imgWidth, imgHeight)
        theCanvas.itemconfigure(imHandler, image=photo)
        theCanvas.pack()
        self.showScreen[choice].update()
        time.sleep(sleepTime)

    def canvasChangePicTest(self, imHandler, imgPath, imgWidth, imgHeight, sleepTime, choice, theCanvas):
        theCanvas = theCanvas[0]
        photo = loadPic(imgPath, imgWidth, imgHeight)
        offsetX = (self.SCREEN_WIDTH - self.SCREEN_HEIGHT * 9 // 10) / 2
        offsetY = 0
        theCanvas.create_image(offsetX, offsetY, image=photo, anchor="nw")
        theCanvas.pack()
        self.showScreen[choice].update()
        # time.sleep(sleepTime)

    def testDelayPosition(self, imHandler, imgWidth, imgHeight, choice, theCanva, rightInts):
        randInts, TrueIndex = creatTestDataset(rightInts)
        randPaths = ['./src/test3/' + str(x) + '.png' for x in randInts]
        print(rightInts)
        for i, path in enumerate(randPaths):
            path = './src/globle/black.png'
            self.canvasChangePicTest(imHandler, path, imgWidth, imgHeight, 0, choice, theCanva)
            self.logger.logImgShow(path, addTrack=True)
            self.CURRENTINDEX = rightInts[i]
            self.controlVal[choice]['state'] = 1
            self.LOCK = False
            theCanva[0].wait_variable(self.controlVal[choice]['IntVar'])
            self.controlVal[choice]['state'] = 0
            newPath = './src/test3/' + str(self.USETCHOICE) + '.png'
            self.canvasChangePic(imHandler, newPath, imgWidth, imgHeight, 0.1, choice, theCanva)

    def RandomShow(self, imHandler, imgWidth, imgHeight, choice, theCanvas):
        randInts = createShowDataset()
        randPaths = ['./src/globle/' + str(x) + '.png' for x in randInts]
        for path in randPaths:
            self.canvasChangePic(imHandler, path, imgWidth, imgHeight, 1, choice, theCanvas)
            self.logger.logImgShow(path, addTrack=False)
        self.logger.logSomething("\n", addTime=False)
        return randInts

    def practice(self):
        self.controlVal[PRACTICE]['state'] = 0
        self.CURRENTTRUE = False
        self.showScreen[PRACTICE].deiconify()
        self.showScreen[PRACTICE].protocol('WM_DELETE_WINDOW', lambda: self.destroy(PRACTICE))
        self.showScreen[PRACTICE].title("延迟回忆-位置练习")
        self.showScreen[PRACTICE].resizable(0, 0)
        buttonCanvas = Canvas(self.showScreen[PRACTICE], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT // 10)
        button1 = Button(buttonCanvas, text='暂停', width=30, height=2,
                         command=lambda: messagebox.showinfo("暂停", "点击确定继续练习"))
        button2 = Button(buttonCanvas, text='退出', width=30, height=2, command=lambda: self.destroy(PRACTICE))
        button1.grid(row=1, column=1)
        button2.grid(row=1, column=2)
        mainCanvas = []
        mainCanvas.append(
            Canvas(self.showScreen[PRACTICE], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT * 9 // 10, bg='black'))
        photo = loadPic(r'./src/globle/start.png', self.SCREEN_HEIGHT * 9 // 10,
                        self.SCREEN_HEIGHT * 9 // 10)
        offsetX = (self.SCREEN_WIDTH - self.SCREEN_HEIGHT * 9 // 10) / 2
        offsetY = 0
        imPractice = mainCanvas[0].create_image(offsetX, offsetY, image=photo, anchor="nw")
        mainCanvas[0].pack()
        buttonCanvas.pack()
        self.showScreen[PRACTICE].update()
        mainCanvas[0].focus_set()
        mainCanvas[0].bind_all("<Key>", self.waitPracticeClick)
        mainCanvas[0].bind_all("<Button-1>", self.waitPracticeClick)
        self.showScreen[PRACTICE].wait_variable(self.controlVal[PRACTICE]['IntVar'])
        self.canvasChangePic(imPractice, './src/test3/delay_recover_location.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 3, PRACTICE, mainCanvas)
        # ####################
        # # 延迟识别-位置
        # ###################
        for _ in range(1):
            # 1.屏幕中央出现一个十字
            self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 2, PRACTICE, mainCanvas)
            # # 2. 随机出现四张图片
            rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
                                        PRACTICE, mainCanvas)
            # # 3. 出现一次白屏和一次黑屏
            self.canvasChangePic(imPractice, './src/globle/white.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 0.1, PRACTICE, mainCanvas)
            self.canvasChangePic(imPractice, './src/globle/black.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 3, PRACTICE, mainCanvas)
            # 4. 测试阶段
            mainCanvas[0].pack()
            mainCanvas[0].focus_set()
            self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, PRACTICE,
                                   mainCanvas, rightInts)
        print(self.logger.getTestAcc(select="mouse"))
        print(self.logger.getAvgActTime(select="mouse"))
        self.logger.logFileString.flush()
        messagebox.showinfo("测试结束", "测试已经结束，感谢您的使用！")
        self.destroy(PRACTICE)
        self.showScreen[PRACTICE].mainloop()

    def realTest(self):
        self.controlVal[REALTEST]['state'] = 0
        self.CURRENTTRUE = False
        self.showScreen[REALTEST].deiconify()
        self.showScreen[REALTEST].protocol('WM_DELETE_WINDOW', lambda: self.destroy(REALTEST))
        self.showScreen[REALTEST].title("延迟回忆-位置测试")
        self.showScreen[REALTEST].resizable(0, 0)
        buttonCanvas = Canvas(self.showScreen[REALTEST], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT // 10)
        button1 = Button(buttonCanvas, text='暂停', width=30, height=2,
                         command=lambda: messagebox.showinfo("暂停", "点击确定继续测试"))
        button2 = Button(buttonCanvas, text='退出', width=30, height=2, command=lambda: self.destroy(REALTEST))
        button1.grid(row=1, column=1)
        button2.grid(row=1, column=2)
        mainCanvas = []
        mainCanvas.append(
            Canvas(self.showScreen[REALTEST], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT * 9 // 10, bg='black'))
        photo = loadPic(r'./src/globle/start.png', self.SCREEN_HEIGHT * 9 // 10,
                        self.SCREEN_HEIGHT * 9 // 10)
        offsetX = (self.SCREEN_WIDTH - self.SCREEN_HEIGHT * 9 // 10) / 2
        offsetY = 0
        imPractice = mainCanvas[0].create_image(offsetX, offsetY, image=photo, anchor="nw")
        mainCanvas[0].pack()
        buttonCanvas.pack()
        self.showScreen[REALTEST].update()
        mainCanvas[0].focus_set()
        mainCanvas[0].bind_all("<Key>", self.waitRealTestClick)
        mainCanvas[0].bind_all("<Button-1>", self.waitRealTestClick)
        self.showScreen[REALTEST].wait_variable(self.controlVal[REALTEST]['IntVar'])
        self.canvasChangePic(imPractice, './src/test3/delay_recover_location.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 3, REALTEST, mainCanvas)
        # ####################
        # # 延迟识别-位置
        # ###################
        for _ in range(20):
            # 1.屏幕中央出现一个十字
            self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 2, REALTEST, mainCanvas)
            # # 2. 随机出现四张图片
            rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
                                        REALTEST, mainCanvas)
            # # 3. 出现一次白屏和一次黑屏
            self.canvasChangePic(imPractice, './src/globle/white.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 0.1, REALTEST, mainCanvas)
            self.canvasChangePic(imPractice, './src/globle/black.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 3, REALTEST, mainCanvas)
            # 4. 测试阶段
            mainCanvas[0].pack()
            mainCanvas[0].focus_set()
            self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, REALTEST,
                                   mainCanvas, rightInts)
        print(self.logger.getTestAcc(select="mouse"))
        print(self.logger.getAvgActTime(select="mouse"))
        self.logger.logFileString.flush()
        messagebox.showinfo("测试结束", "测试已经结束，感谢您的使用！")
        self.destroy(REALTEST)
        self.showScreen[REALTEST].mainloop()

def Entrance():
    master = Tk()
    master.title("延迟回忆-位置")
    master.geometry('500x250')
    master.resizable(0, 0)
    frame = Frame(master=master, width=100, height=20).pack()
    label = Label(master=frame, text="延迟回忆-位置", width=30, height=2, font=('黑体', 20))
    label.pack()
    mainprocess = mainProcess()
    button_1 = Button(master=frame, text="开始练习", width=30, height=4, command=mainprocess.practice)
    button_1.pack()
    button_2 = Button(master=frame, text="开始检测", width=30, height=4, command=mainprocess.realTest)
    button_2.pack()
    master.mainloop()
    mainprocess.logger.logFileString.close()


if __name__ == '__main__':
    Entrance()
