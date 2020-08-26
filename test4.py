# 位置-练习

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
        self.datasetControl = None
        # self.logger = Logger(saveFilePath="test4.log")
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

    def destroy(self, choice, output=True):
        self.showScreen[choice].destroy()
        self.showScreen[choice] = Toplevel()
        self.showScreen[choice].withdraw()
        self.controlVal[choice]['state'] = 0
        if choice == PRACTICE:
            self.controlVal[choice]['IntVar'] = IntVar(self.showScreen[choice], 0, name="PRACTICE")
        else:
            self.controlVal[choice]['IntVar'] = IntVar(self.showScreen[choice], 0, name="REALTEST")
        self.controlVal[choice]['value'] = 0
        if output:
            print(self.logger.getTestAcc(select="key"))
            print(self.logger.getAvgActTime(select="key"))
        self.logger.logFileString.flush()
        self.logger.logFileString.close()
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

    def testDelayPosition(self, imHandler, imgWidth, imgHeight, choice, theCanva, rightInts, epoch):
        randInts, TrueIndex = self.datasetControl.getTestDatasetByIndex(epoch)
        randPaths = ['./src/test4/' + x for x in randInts]
        for i, path in enumerate(randPaths):
            self.canvasChangePicTest(imHandler, path, imgWidth, imgHeight, 1, choice, theCanva)
            self.logger.logImgShow(path, addTrack=True)
            if i in TrueIndex:
                self.CURRENTTRUE = True
            else:
                self.CURRENTTRUE = False
            self.LOCK = False
            theCanva[0].wait_variable(self.controlVal[choice]['IntVar'])
            # self.canvasChangePic(imHandler, './src/test4/block.png', imgWidth, imgHeight, 0.05, choice, theCanva)
        self.logger.logSomething("\n", addTime=False)

    def RandomShow(self, imHandler, imgWidth, imgHeight, choice, theCanvas, epoch):
        randInts = self.datasetControl.getShowDatasetByIndex(epoch)
        randPaths = ['./src/test4/' + x for x in randInts]
        for path in randPaths:
            self.canvasChangePic(imHandler, path, imgWidth, imgHeight, 1, choice, theCanvas)
            self.logger.logImgShow(path, addTrack=False)
        self.logger.logSomething("\n", addTime=False)
        return randInts

    def practice(self):
        prefixPath = './log/test4/practice/'
        code = self.init_usernamename()
        if code == -1:
            return
        savepath = prefixPath + self.date + '-' + self.name + '-练习日志.log'
        savepath.replace(' ', '')
        self.logger = Logger(saveFilePath=savepath)
        self.logger.logSomething("**********开始练习：位置-练习**********")
        self.controlVal[PRACTICE]['state'] = 0
        self.CURRENTTRUE = False
        self.showScreen[PRACTICE].deiconify()
        self.showScreen[PRACTICE].protocol('WM_DELETE_WINDOW', lambda :self.destroy(PRACTICE))
        self.showScreen[PRACTICE].title("位置-练习(练习)")
        self.showScreen[PRACTICE].resizable(0, 0)
        buttonCanvas = Canvas(self.showScreen[PRACTICE], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT//10)
        button1 = Button(buttonCanvas, text='暂停', width=30, height=2, command=lambda: messagebox.showinfo("暂停", "点击右下方OK继续练习"))
        button2 = Button(buttonCanvas, text='退出', width=30, height=2, command=lambda: self.destroy(PRACTICE))
        button1.grid(row=1, column=1)
        button2.grid(row=1, column=2)
        mainCanvas = []
        mainCanvas.append(Canvas(self.showScreen[PRACTICE], width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT*9//10, bg='black'))
        photo = loadPic(r'./src/test4/start.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10)
        offsetX = (self.SCREEN_WIDTH - self.SCREEN_HEIGHT*9//10) / 2
        offsetY = 0
        imPractice = mainCanvas[0].create_image(offsetX, offsetY, image=photo, anchor="nw")
        mainCanvas[0].pack()
        buttonCanvas.pack()
        self.canvasChangePic(imPractice, r'./src/test4/start.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 3, PRACTICE, mainCanvas)
        self.showScreen[PRACTICE].update()
        self.canvasChangePic(imPractice, r'./src/test4/location_delay_recognition.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 0, PRACTICE, mainCanvas)
        mainCanvas[0].focus_set()
        mainCanvas[0].bind("<Key>", self.waitPracticeConfirm)
        self.showScreen[PRACTICE].wait_variable(self.controlVal[PRACTICE]['IntVar'])
        # ####################
        # # 延迟识别-位置
        # ###################
        # 负荷 2
        flag_2 = False
        while True:
            self.logger.imgShowInfoList = []
            self.logger.keyPressInfoList = []
            self.logger.mouseClickInfoList = []
            if not flag_2:
                messagebox.showinfo("负荷2测试", "负荷2测试共计2轮，点击右下OK继续！")
            self.datasetControl = test4DatasetControl()
            self.datasetControl.createShowDataset(2, 2)
            self.datasetControl.createTestDataset()
            for _ in range(2):
                # 1.屏幕中央出现一个十字
                self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 2, PRACTICE, mainCanvas)
                # 2. 随机出现四张图片
                rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, PRACTICE, mainCanvas, _)
                # 3. 出现一次白屏和一次黑屏
                self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH, self.SCREEN_HEIGHT*9//10, 0.1, PRACTICE, mainCanvas)
                self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, 3, PRACTICE, mainCanvas)
                # 4. 测试阶段
                mainCanvas[0].pack()
                mainCanvas[0].focus_set()
                self.testDelayPosition(imPractice, self.SCREEN_HEIGHT*9//10, self.SCREEN_HEIGHT*9//10, PRACTICE, mainCanvas, rightInts, _)

            acc1 = self.logger.getTestAcc(select='key', write=False)

            if acc1 < 0.60:
                self.logger.logSomething("***********2张图片测试结果(未通过)************", False)
                self.logger.logSomething("\nACC < 60%; Again!\n", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                messagebox.showinfo("负荷2测试未通过", "测试未通过({:.2%})重新测试共计2轮，点击右下OK继续！".format(acc1))
                flag_2 = True
            else:
                self.logger.logSomething("***********2张图片测试结果(通过)************", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                flag_2 = False
                break

        flag_3 = False
        while True:
            self.logger.logFileString.flush()
            self.logger.imgShowInfoList = []
            self.logger.keyPressInfoList = []
            self.logger.mouseClickInfoList = []
            if not flag_3:
                messagebox.showinfo("负荷3测试", "负荷3测试共计4轮，点击右下OK继续！")
            self.datasetControl = test4DatasetControl()
            self.datasetControl.createShowDataset(4, 3)
            self.datasetControl.createTestDataset()
            for _ in range(4):
                # 1.屏幕中央出现一个十字
                self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 2, PRACTICE, mainCanvas)
                # 2. 随机出现四张图片
                rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
                                            PRACTICE, mainCanvas, _)
                # 3. 出现一次白屏和一次黑屏
                self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH,
                                     self.SCREEN_HEIGHT * 9 // 10, 0.1, PRACTICE, mainCanvas)
                self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 3, PRACTICE, mainCanvas)
                # 4. 测试阶段
                mainCanvas[0].pack()
                mainCanvas[0].focus_set()
                self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, PRACTICE,
                                       mainCanvas, rightInts, _)

            acc1 = self.logger.getTestAcc(select='key', write=False)
            # self.logger.getAvgActTime(select='key')
            if acc1 < 0.60:
                self.logger.logSomething("***********3张图片测试结果(未通过)************", False)
                self.logger.logSomething("\nACC < 60%; Again!\n", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                messagebox.showinfo("负荷3测试未通过", "测试未通过({:.2%})重新测试共计4轮，点击右下OK继续！".format(acc1))
                flag_3 = True
            else:
                self.logger.logSomething("***********3张图片测试结果(通过)************", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                flag_3 = False
                break

        self.logger.logSomething("\n",False)

        flag_4 = False
        while True:
            self.logger.logFileString.flush()
            self.logger.imgShowInfoList = []
            self.logger.keyPressInfoList = []
            self.logger.mouseClickInfoList = []
            if not flag_4:
                messagebox.showinfo("负荷4测试", "负荷4测试共计2轮，点击右下OK继续！")
            self.datasetControl = test4DatasetControl()
            self.datasetControl.createShowDataset(2, 4)
            self.datasetControl.createTestDataset()
            for _ in range(2):
                # 1.屏幕中央出现一个十字
                self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 2, PRACTICE, mainCanvas)
                # 2. 随机出现四张图片
                rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
                                            PRACTICE, mainCanvas, _)
                # 3. 出现一次白屏和一次黑屏
                self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH,
                                     self.SCREEN_HEIGHT * 9 // 10, 0.1, PRACTICE, mainCanvas)
                self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 3, PRACTICE, mainCanvas)
                # 4. 测试阶段
                mainCanvas[0].pack()
                mainCanvas[0].focus_set()
                self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, PRACTICE,
                                   mainCanvas, rightInts, _)

            acc1 = self.logger.getTestAcc(select='key', write=False)
            # self.logger.getAvgActTime(select='key')
            if acc1 < 0.60:
                self.logger.logSomething("***********4张图片测试结果(未通过)************", False)
                self.logger.logSomething("\nACC < 60%; Again!\n", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                messagebox.showinfo("负荷4测试未通过", "测试未通过({:.2%})重新测试共计2轮，点击右下OK继续！".format(acc1))
                flag_4 = True
            else:
                self.logger.logSomething("***********4张图片测试结果(通过)************", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                flag_4 = False
                break

        messagebox.showinfo("测试结束", "测试已经结束，感谢您的使用！")
        self.destroy(PRACTICE, output=False)
        self.showScreen[PRACTICE].mainloop()

    def realTest(self):
        prefixPath = './log/test4/'
        code = self.init_usernamename()
        if code == -1:
            return
        savepath = prefixPath + self.date + '-' + self.name + '-测试日志.log'
        self.logger = Logger(saveFilePath=savepath)
        self.logger.logSomething("**********开始练习：位置-练习**********")
        self.controlVal[REALTEST]['state'] = 0
        self.CURRENTTRUE = False

        self.showScreen[REALTEST].deiconify()
        self.showScreen[REALTEST].protocol('WM_DELETE_WINDOW', lambda: self.destroy(REALTEST))
        self.showScreen[REALTEST].title("位置-练习")
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
        photo = loadPic(r'./src/test4/start.png', self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10)
        offsetX = (self.SCREEN_WIDTH - self.SCREEN_HEIGHT * 9 // 10) / 2
        offsetY = 0
        imPractice = mainCanvas[0].create_image(offsetX, offsetY, image=photo, anchor="nw")
        mainCanvas[0].pack()
        buttonCanvas.pack()
        self.canvasChangePic(imPractice, r'./src/test4/start.png', self.SCREEN_HEIGHT * 9 // 10,
                             self.SCREEN_HEIGHT * 9 // 10, 3, REALTEST, mainCanvas)
        self.showScreen[REALTEST].update()
        self.canvasChangePic(imPractice, r'./src/test4/location_delay_recognition.png', self.SCREEN_HEIGHT * 9 // 10,
                             self.SCREEN_HEIGHT * 9 // 10, 0, REALTEST, mainCanvas)
        mainCanvas[0].focus_set()
        mainCanvas[0].bind("<Key>", self.waitRealTestConfirm)
        self.showScreen[REALTEST].wait_variable(self.controlVal[REALTEST]['IntVar'])
        # ####################
        # # 延迟识别-位置
        # ###################
        flag_2 = False
        while True:
            self.logger.logFileString.flush()
            self.logger.imgShowInfoList = []
            self.logger.keyPressInfoList = []
            self.logger.mouseClickInfoList = []

            self.datasetControl = test4DatasetControl()
            self.datasetControl.createShowDataset(20, 2)
            self.datasetControl.createTestDataset()
            if not flag_2:
                messagebox.showinfo("负荷2测试", "负荷2测试共计20轮，点击右下OK继续！")

            for _ in range(20):
                # 1.屏幕中央出现一个十字
                self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 2, REALTEST, mainCanvas)
                # 2. 随机出现四张图片
                rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
                                            REALTEST, mainCanvas, _)
                # 3. 出现一次白屏和一次黑屏
                self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH,
                                     self.SCREEN_HEIGHT * 9 // 10, 0.1, REALTEST, mainCanvas)
                self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 3, REALTEST, mainCanvas)
                # 4. 测试阶段
                mainCanvas[0].pack()
                mainCanvas[0].focus_set()
                self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, REALTEST,
                                       mainCanvas, rightInts, _)

            acc1 = self.logger.getTestAcc(select='key',write=False)
            # self.logger.getAvgActTime(select='key')
            if acc1 < 0.60:
                self.logger.logSomething("***********2张图片测试结果(未通过)************", False)
                self.logger.logSomething("\nACC < 60%; Again!\n", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                messagebox.showinfo("负荷2测试未通过", "测试未通过({:.2%})重新测试共计20轮，点击右下OK继续！".format(acc1))
                flag_2 = True
            else:
                self.logger.logSomething("***********2张图片测试结果(通过)************", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                flag_2 = False
                break

        flag_3 = False
        while True:
            self.logger.logSomething("\n", False)
            self.logger.logFileString.flush()
            self.logger.imgShowInfoList = []
            self.logger.keyPressInfoList = []
            self.logger.mouseClickInfoList = []

            self.datasetControl = test4DatasetControl()
            self.datasetControl.createShowDataset(20, 3)
            self.datasetControl.createTestDataset()
            if not flag_3:
                messagebox.showinfo("负荷3测试", "负荷3测试共计20轮，点击右下OK继续！")
            for _ in range(20):
                # 1.屏幕中央出现一个十字
                self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 2, REALTEST, mainCanvas)
                # 2. 随机出现四张图片
                rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
                                            REALTEST, mainCanvas, _)
                # 3. 出现一次白屏和一次黑屏
                self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH,
                                     self.SCREEN_HEIGHT * 9 // 10, 0.1, REALTEST, mainCanvas)
                self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT * 9 // 10,
                                     self.SCREEN_HEIGHT * 9 // 10, 3, REALTEST, mainCanvas)
                # 4. 测试阶段
                mainCanvas[0].pack()
                mainCanvas[0].focus_set()
                self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, REALTEST,
                                       mainCanvas, rightInts, _)

            acc1 = self.logger.getTestAcc(select='key', write=False)
            # self.logger.getAvgActTime(select='key')
            self.logger.logSomething("\n",False)
            if acc1 < 0.60:
                self.logger.logSomething("***********3张图片测试结果(未通过)************", False)
                self.logger.logSomething("\nACC < 60%; Again!\n", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                messagebox.showinfo("负荷3测试未通过", "测试未通过({:.2%})重新测试共计20轮，点击右下OK继续！".format(acc1))
                flag_3 = True
            else:
                self.logger.logSomething("***********3张图片测试结果(通过)************", False)
                self.logger.getTestAcc(select='key')
                self.logger.getAvgActTime(select='key')
                self.logger.logSomething("******************************************", False)
                self.logger.logFileString.flush()
                flag_3 = False
                break
        # flag_4 = False
        # while True:
        #     self.logger.logFileString.flush()
        #     self.logger.imgShowInfoList = []
        #     self.logger.keyPressInfoList = []
        #     self.logger.mouseClickInfoList = []
        #
        #     self.datasetControl = test4DatasetControl()
        #     self.datasetControl.createShowDataset(20, 4)
        #     self.datasetControl.createTestDataset()
        #     if not flag_4:
        #         messagebox.showinfo("负荷4测试", "负荷4测试共计20轮，点击右下OK继续！")
        #     for _ in range(20):
        #         # 1.屏幕中央出现一个十字
        #         self.canvasChangePic(imPractice, r'./src/globle/1_16.png', self.SCREEN_HEIGHT * 9 // 10,
        #                              self.SCREEN_HEIGHT * 9 // 10, 2, REALTEST, mainCanvas)
        #         # 2. 随机出现四张图片
        #         rightInts = self.RandomShow(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10,
        #                                     REALTEST, mainCanvas, _)
        #         # 3. 出现一次白屏和一次黑屏
        #         self.canvasChangePic_(imPractice, './src/globle/white.png', self.SCREEN_WIDTH,
        #                              self.SCREEN_HEIGHT * 9 // 10, 0.1, REALTEST, mainCanvas)
        #         self.canvasChangePic(imPractice, './src/globle/black_word.png', self.SCREEN_HEIGHT * 9 // 10,
        #                              self.SCREEN_HEIGHT * 9 // 10, 3, REALTEST, mainCanvas)
        #         # 4. 测试阶段
        #         mainCanvas[0].pack()
        #         mainCanvas[0].focus_set()
        #         self.testDelayPosition(imPractice, self.SCREEN_HEIGHT * 9 // 10, self.SCREEN_HEIGHT * 9 // 10, REALTEST,
        #                                mainCanvas, rightInts, _)
        #
        #     acc1 = self.logger.getTestAcc(select='key', write=False)
        #     # self.logger.getAvgActTime(select='key')
        #     self.logger.logSomething("\n", False)
        #     if acc1 < 0.60:
        #         self.logger.logSomething("***********4张图片测试结果(未通过)************", False)
        #         self.logger.logSomething("\nACC < 60%; Again!\n", False)
        #         self.logger.getTestAcc(select='key')
        #         self.logger.getAvgActTime(select='key')
        #         self.logger.logSomething("******************************************", False)
        #         self.logger.logFileString.flush()
        #         messagebox.showinfo("负荷4测试未通过", "测试未通过({:.2%})重新测试共计20轮，点击右下OK继续！".format(acc1))
        #         flag_4 = True
        #     else:
        #         self.logger.logSomething("***********4张图片测试结果(通过)************", False)
        #         self.logger.getTestAcc(select='key')
        #         self.logger.getAvgActTime(select='key')
        #         self.logger.logSomething("******************************************", False)
        #         self.logger.logFileString.flush()
        #         flag_4 = False
        #         break

        # print(self.logger.getTestAcc(select="key"))
        # print(self.logger.getAvgActTime(select="key"))
        self.logger.logFileString.flush()
        # messagebox.showinfo("测试结束", "测试已经结束，感谢您的使用！")
        self.destroy(REALTEST, output=False)
        self.showScreen[REALTEST].mainloop()

def Entrance():
    master = Tk()
    master.title("位置-练习")
    master.geometry('500x300')
    master.resizable(0, 0)
    frame = Frame(master=master, width=100, height=24).pack()
    label = Label(master=frame, text="位置-练习", width=30, height=2, font=('黑体', 20))
    label.pack()
    label2 = Label(master=frame, text="请输入用户名:")
    label2.pack()
    entry = Entry(master=frame, width=30)
    entry.pack()
    mainprocess = mainProcess(entry)
    # button_1 = Button(master=frame, text="开始练习", width=30, height=4, command=mainprocess.practice)
    # button_1.pack()
    button_2 = Button(master=frame, text="开始练习", width=30, height=4, command=mainprocess.realTest)
    button_2.pack()
    master.mainloop()


if __name__ == '__main__':
    Entrance()