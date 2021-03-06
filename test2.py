# 延迟识别-言语

from tkinter import *
from tkinter import messagebox

from utils import *
import random
import datetime

PRACTICE = 0
REALTEST = 1

class mainProcess:
    def __init__(self,user):
        self.showScreen = [Toplevel(), Toplevel()]
        for o in self.showScreen:
            o.withdraw()
        self.controlVal = [{'value': 0, 'IntVar': IntVar(self.showScreen[PRACTICE], 0, name="PRACTICE"), 'state': 0},
                           {'value': 0, 'IntVar': IntVar(self.showScreen[REALTEST], 0, name="REALTEST"), 'state': 0}]
        self.SCREEN_WIDTH = self.showScreen[PRACTICE].winfo_screenwidth()
        self.SCREEN_HEIGHT = self.showScreen[PRACTICE].winfo_screenheight()
        self.CURRENTTRUE = False
        # self.logger = Logger(saveFilePath='test2.log')
        self.LOCK = None
        self.name = ""
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.user = user
        # self.logger = None
        createLogDirection()

    def init_usernamename(self):
        username = self.user.get().__str__()
        if username == '':
            messagebox.showinfo("Warning", "请输入用户名！")
            return -1
        self.name = username
        return 0

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
        print(self.logger.getTestAcc(select="key"))
        print(self.logger.getAvgActTime(select="key"))
        self.logger.logFileString.flush()
        self.logger.closeFile()
        messagebox.showinfo("测试结束", "测试已经结束，感谢您的使用！")


    def waitPracticeConfirm(self, event):
        if event.char == ' ' and self.controlVal[PRACTICE]['state'] == 0:
            self.controlVal[PRACTICE]['state'] = 1
            self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[PRACTICE], 1, name="PRACTICE")
            self.controlVal[PRACTICE]['value'] = 1
            return
        if event.char in ['1', '2'] and self.controlVal[PRACTICE]['state'] == 1 and self.LOCK == False:
            self.LOCK = True
            if self.controlVal[PRACTICE]['value'] == 0:
                self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[PRACTICE], 1, name="PRACTICE")
                self.controlVal[PRACTICE]['value'] = 1
            elif self.controlVal[PRACTICE]['value'] == 1:
                self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[PRACTICE], 0, name="PRACTICE")
                self.controlVal[PRACTICE]['value'] = 0

            if (self.CURRENTTRUE is True and (event.char is '1')) or \
                    (self.CURRENTTRUE is False and (event.char is '2')):
                print("正确！")
                self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='1')
            else:
                print("错误！")
                self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='0')


    def waitRealTestConfirm(self, event):
        if event.char == ' ' and self.controlVal[REALTEST]['state'] == 0:
            self.controlVal[REALTEST]['state'] = 1
            self.controlVal[REALTEST]['IntVar'] = IntVar(self.showScreen[REALTEST], 1, name="REALTEST")
            self.controlVal[REALTEST]['value'] = 1
            return
        if event.char in ['1', '2'] and self.controlVal[REALTEST]['state'] == 1 and self.LOCK == False:
            self.LOCK = True
            if self.controlVal[PRACTICE]['value'] == 0:
                self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[REALTEST], 1, name="REALTEST")
                self.controlVal[PRACTICE]['value'] = 1
            elif self.controlVal[PRACTICE]['value'] == 1:
                self.controlVal[PRACTICE]['IntVar'] = IntVar(self.showScreen[REALTEST], 0, name="REALTEST")
                self.controlVal[PRACTICE]['value'] = 0

            if (self.CURRENTTRUE is True and (event.char is '1')) or \
                    (self.CURRENTTRUE is False and (event.char is '2')):
                print("正确！")
                self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='1')
            else:
                print("错误！")
                self.logger.logPressKey(theKey=event.char, addTrack=TRUE, isCrorrect='0')

    def canvasChangePic(self, imHandler, imgPath, imgWidth, imgHeight, sleepTime, choice, theCanvas):
        theCanvas = theCanvas[0]
        photo = loadPic(imgPath, imgWidth, imgHeight)
        theCanvas.itemconfigure(imHandler, image=photo)
        theCanvas.pack()
        self.showScreen[choice].update()
        time.sleep(sleepTime)

    def canvasChangePic_(self, imHandler, imgPath, imgWidth, imgHeight, sleepTime, choice, theCanvas):
        theCanvas = theCanvas[0]
        photo = loadPic_(imgPath, imgWidth, imgHeight)
        theCanvas.create_image(0,0,image=photo, anchor="nw")
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

    def testDelayPosition(self, imHandler, imgWidth, imgHeight, choice, theCanva, testImg, trueMask):
        randInts = testImg
        randPaths = ['./src/test2/' + str(x) + '.png' for x in randInts]
        for i, path in enumerate(randPaths):
            self.canvasChangePicTest(imHandler, path, imgWidth, imgHeight, 1, choice, theCanva)
            self.logger.logImgShow(path, addTrack=True)
            if trueMask[i] == 1:
                self.CURRENTTRUE = True
            else:
                self.CURRENTTRUE = False
            self.LOCK = False
            theCanva[0].wait_variable(self.controlVal[choice]['IntVar'])
        self.logger.logSomething("\n", addTime=False)

    def RandomShow(self, imHandler, imgWidth, imgHeight, choice, theCanvas, showImg):
        randInts = showImg
        randPaths = ['./src/test2/' + str(x) + '.png' for x in randInts]
        for path in randPaths:
            self.canvasChangePic(imHandler, path, imgWidth, imgHeight, 1, choice, theCanvas)
            self.logger.logImgShow(path, addTrack=False)
        self.logger.logSomething("\n", addTime=False)
        return randInts

    def practice(self):
        prefixPath = './log/test2/practice/'
        code = self.init_usernamename()
        if code == -1:
            return
        savepath = prefixPath + self.date + '-' + self.name + '-练习日志.log'
        savepath.replace(' ','')
        self.logger = Logger(saveFilePath=savepath)
        self.logger.logSomething("**********开始练习：延迟识别-言语**********")
        self.controlVal[PRACTICE]['state'] = 0
        self.CURRENTTRUE = False
        self.showScreen[PRACTICE].deiconify()
        self.showScreen[PRACTICE].protocol('WM_DELETE_WINDOW', lambda :self.destroy(PRACTICE))
        self.showScreen[PRACTICE].title("延迟识别-言语练习")
        self.showScreen[PRACTICE].resizable(0, 0)
        buttonCanvas = Canvas(self.showScreen[PRACTICE], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT//10)
        button1 = Button(buttonCanvas, text='暂停', width=30, height=2, command=lambda: messagebox.showinfo("暂停", "点击右下角OK继续练习"))
        button2 = Button(buttonCanvas, text='退出', width=30, height=2, command=lambda: self.destroy(PRACTICE))
        button1.grid(row=1, column=1)
        button2.grid(row=1, column=2)
        mainCanvas = []
        mainCanvas.append(Canvas(self.showScreen[PRACTICE], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT*9//10, bg='black'))
        photo = loadPic(r'./src/test2/start.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10)
        offsetX = (self.SCREEN_WIDTH - self.SCREEN_HEIGHT*9//10) / 2
        offsetY = 0
        imPractice = mainCanvas[0].create_image(offsetX, offsetY, image=photo, anchor="nw")
        mainCanvas[0].pack()
        buttonCanvas.pack()
        self.canvasChangePic(imPractice, r'./src/test2/start.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 3, PRACTICE, mainCanvas)
        self.showScreen[PRACTICE].update()
        self.canvasChangePic(imPractice, r'./src/test2/delay_recognition_number.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 1, PRACTICE, mainCanvas)
        mainCanvas[0].focus_set()
        mainCanvas[0].bind("<Key>", self.waitPracticeConfirm)
        self.showScreen[PRACTICE].wait_variable(self.controlVal[PRACTICE]['IntVar'])
        # ####################
        # # 延迟识别-位置
        # ###################
        messagebox.showinfo("负荷4测试", "负荷4测试共计1轮，点击右下OK继续！")
        for _ in range(1):
            showImg, testImg, trueMask = get2or3or4Imgs(4, imgTotalCount=10)
            # 1.屏幕中央出现一个十字
            self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 2, PRACTICE, mainCanvas)
            # 2. 随机出现四张图片
            rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, PRACTICE, mainCanvas, showImg)
            # 3. 出现一次白屏和一次黑屏
            self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH, self.SCREEN_HEIGHT*9//10, 0.1, PRACTICE, mainCanvas)
            self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 3, PRACTICE, mainCanvas)
            # 4. 测试阶段
            mainCanvas[0].pack()
            mainCanvas[0].focus_set()
            self.testDelayPosition(imPractice, self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, PRACTICE, mainCanvas, testImg, trueMask)

        # print(self.logger.getTestAcc(select="key"))
        # print(self.logger.getAvgActTime(select="key"))
        self.logger.logFileString.flush()
        # messagebox.showinfo("测试结束", "测试已经结束，感谢您的使用！")
        self.destroy(PRACTICE)
        self.showScreen[PRACTICE].mainloop()

    def realTest(self):
        prefixPath = './log/test2/realtest/'
        code = self.init_usernamename()
        if code == -1:
            return
        savepath = prefixPath + self.date + '-' + self.name + '-测试日志.log'
        self.logger = Logger(saveFilePath=savepath)
        self.logger.logSomething("**********开始测试：延迟识别-言语**********")
        self.controlVal[REALTEST]['state'] = 0
        self.CURRENTTRUE = False

        self.showScreen[REALTEST].deiconify()
        self.showScreen[REALTEST].protocol('WM_DELETE_WINDOW', lambda: self.destroy(REALTEST))
        self.showScreen[REALTEST].title("延迟识别-言语测试")
        self.showScreen[REALTEST].resizable(0, 0)
        buttonCanvas = Canvas(self.showScreen[REALTEST], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT // 10)
        button1 = Button(buttonCanvas, text='暂停', width=30, height=2,
                         command=lambda: messagebox.showinfo("暂停", "点击右下方OK继续测试"))
        button2 = Button(buttonCanvas, text='退出', width=30, height=2, command=lambda: self.destroy(REALTEST))
        button1.grid(row=1, column=1)
        button2.grid(row=1, column=2)
        mainCanvas = []
        mainCanvas.append(
            Canvas(self.showScreen[REALTEST], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT * 9 // 10, bg='black'))
        photo = loadPic(r'./src/test2/start.png', self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10)
        offsetX = (self.SCREEN_WIDTH - self.SCREEN_HEIGHT * 9 // 10) / 2
        offsetY = 0
        imPractice = mainCanvas[0].create_image(offsetX, offsetY, image=photo, anchor="nw")
        mainCanvas[0].pack()
        buttonCanvas.pack()
        self.canvasChangePic(imPractice, r'./src/test2/start.png', self.SCREEN_HEIGHT * 9 // 10,
                             self.SCREEN_HEIGHT * 9 // 10, 3, REALTEST, mainCanvas)
        self.showScreen[REALTEST].update()
        self.canvasChangePic(imPractice, r'./src/test2/delay_recognition_number.png', self.SCREEN_HEIGHT * 9 // 10,
                             self.SCREEN_HEIGHT * 9 // 10, 1, REALTEST, mainCanvas)
        mainCanvas[0].focus_set()
        mainCanvas[0].bind("<Key>", self.waitRealTestConfirm)
        self.showScreen[REALTEST].wait_variable(self.controlVal[REALTEST]['IntVar'])
        # ####################
        # # 延迟识别-位置
        # ###################
        messagebox.showinfo("负荷4测试", "负荷4测试共计10轮，点击右下OK继续！")
        for _ in range(10):
            showImg, testImg, trueMask = get2or3or4Imgs(4, imgTotalCount=10)
            # 1.屏幕中央出现一个十字
            self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 2, REALTEST, mainCanvas)
            # 2. 随机出现四张图片
            rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
                                        REALTEST, mainCanvas, showImg)
            # 3. 出现一次白屏和一次黑屏
            self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH,
                                 self.SCREEN_HEIGHT * 9 // 10, 0.1, REALTEST, mainCanvas)
            self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT * 9 // 10,
                                 self.SCREEN_HEIGHT * 9 // 10, 3, REALTEST, mainCanvas)
            # 4. 测试阶段
            mainCanvas[0].pack()
            mainCanvas[0].focus_set()
            self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, REALTEST,
                                   mainCanvas, testImg, trueMask)

        # print(self.logger.getTestAcc(select="key"))
        # print(self.logger.getAvgActTime(select="key"))
        self.logger.logFileString.flush()
        # messagebox.showinfo("测试结束", "测试已经结束，感谢您的使用！")
        self.destroy(REALTEST)
        self.showScreen[REALTEST].mainloop()

def Entrance():
    master = Tk()
    master.title("延迟识别-言语")
    master.geometry('500x300')
    master.resizable(0, 0)
    frame = Frame(master=master, width=100, height=24).pack()
    label = Label(master=frame, text="延迟识别-言语", width=30, height=2, font=('黑体', 20))
    label.pack()
    label2 = Label(master=frame, text="请输入用户名:")
    label2.pack()
    entry = Entry(master=frame, width=30)
    entry.pack()
    mainprocess = mainProcess(entry)
    button_1 = Button(master=frame, text="开始练习", width=30, height=4, command=mainprocess.practice)
    button_1.pack()
    button_2 = Button(master=frame, text="开始检测", width=30, height=4, command=mainprocess.realTest)
    button_2.pack()
    master.mainloop()


if __name__ == '__main__':
    Entrance()
