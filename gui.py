from tkinter import *
from tkinter import messagebox
from utils import *
import random

balance = None
balanceShow = None
canvas = None
canvas1Practice = None
GroundTrue = True
# root = None
# root1Master = None
root1 = None
root2 = None
root3 = None
root4 = None
MaxWidth = 0
MaxHeight = 0


def canvasChangePic(im, path, w, h, t,canvas_ = canvas):
    photo = loadPic(path, w, h)
    canvas_.itemconfigure(im, image=photo)
    canvas_.pack()
    root1.update()
    time.sleep(t)


def RandomShow(w, h, im,canvsa_ = canvas):
    """
    随机出现四张图片
    :param w: 图片的宽度
    :param h: 图片的高度
    :param im: canvas的图片对象
    :return: 正确的图片位置
    """
    randInts = []
    lastInt = -1
    while True:
        currentInt = random.randint(0, 15)
        if currentInt != lastInt:
            randInts.append(currentInt)
            lastInt = currentInt
        if len(randInts) == 4:
            break
    randPaths = ['./img/' + str(x) + '.png' for x in randInts]
    for path in randPaths:
        canvasChangePic(im, path, w, h, 1,canvas)
    print(randInts)
    return randInts


def TestDelayPosition(w, h, im, rightInt,canvas_ = canvas):
    """
    测试延迟识别-位置
    :param w: 图片的宽度
    :param h: 图片的高度
    :param im: canvas图像对象
    :param rightInt: 正确图片位置数组
    :return:
    """
    global GroundTrue
    randInts, TrueIndex = creatTestDataset(rightInt)
    randPaths = ['./img/' + str(x) + '.png' for x in randInts]
    for i, path in enumerate(randPaths):
        canvasChangePic(im, path, w, h, 1,canvas_)
        if i == TrueIndex:
            GroundTrue = True
        else:
            GroundTrue = False
        canvas.wait_variable(balance)
    print(randInts)
    return randInts


def waitSpace(event):
    global balance
    print("字符：", event.char)


def waitConfirm(event):
    global balance
    global GroundTrue
    global balanceShow
    if event.char == ' ':
        balance = IntVar(root1, 1, name="balance")
        balanceShow = 1
        return
    if event.char in ['m', 'c']:
        if balanceShow == 0:
            balance = IntVar(root1, 1, name="balance")
            balanceShow = 1
        elif balanceShow == 1:
            balance = IntVar(root1, 0, name="balance")
            balanceShow = 0
        if (event.char == 'm' and GroundTrue == True) or (event.char == 'c' and GroundTrue == False):
            pass
        else:
            pass


def pause():
    messagebox.showinfo("暂停", "点击确定继续练习")


def Step1():
    global canvas
    global root1
    global balance
    global balanceShow
    root1 = Toplevel()
    # root1 = Tk()
    balance = IntVar(root1, 0, name="balance")
    balanceShow = 0
    MaxWidth = root1.winfo_screenwidth()  # 设置窗口最大宽度为屏幕宽度
    MaxHeight = root1.winfo_screenheight() - 10
    root1.title("DMS测试")
    root1.resizable(0, 0)
    canvas = Canvas(root1, width=MaxWidth, height=MaxHeight, bg='black')
    photo = loadPic(r'./img/start.png', MaxHeight, MaxHeight)
    offsetX = (MaxWidth - MaxHeight) / 2
    offsetY = 0
    im = canvas.create_image(offsetX, offsetY, image=photo, anchor="nw")
    canvas.pack()
    root1.update()
    canvas.focus_set()
    canvas.bind("<Key>", waitConfirm)
    root1.wait_variable(balance)
    # 给出测试提示
    canvasChangePic(im, r'img/delay_recognition_location.png', MaxHeight, MaxHeight, 3,canvas_=canvas)
    ####################
    # 延迟识别-位置
    ###################
    for _ in range(20):
        # 1.屏幕中央出现一个十字
        canvasChangePic(im, r'img/1_16.png', MaxHeight, MaxHeight, 2,canvas)
        # 2. 随机出现四张图片
        rightInts = RandomShow(MaxWidth, MaxHeight, im)
        # 3. 出现一次白屏和一次黑屏
        canvasChangePic(im, './img/white.png', MaxWidth, MaxHeight, 0.1,canvas)
        canvasChangePic(im, './img/black.png', MaxWidth, MaxHeight, 3,canvas)
        # 4. 测试阶段
        canvas.pack()
        canvas.focus_set()
        TestDelayPosition(MaxWidth, MaxHeight, im, rightInts,canvas)
    # root1.mainloop()


def Step1Practice():
    global canvas1Practice
    global balance
    global balanceShow
    top = Toplevel()
    balance = IntVar(top, 0, name="balance")
    balanceShow = 0
    w = top.winfo_screenwidth()
    h = top.winfo_screenheight() - 100
    top.title("延迟识别-位置练习")
    top.resizable(0, 0)
    canvastemp = Canvas(top, width=w, height=40, bg='black')
    button1 = Button(canvastemp, text='暂停', width=30, height=2, command=pause)
    button2 = Button(canvastemp, text='退出', width=30, height=2, command=lambda: top.destroy())
    button1.grid(row=1, column=1)
    button2.grid(row=1, column=2)
    canvas1Practice = Canvas(top, width=w, height=h, bg='black')
    photo = loadPic(r'./img/start.png', h, h)
    offsetX = (w - h) / 2
    offsetY = 0
    imPractice = canvas1Practice.create_image(offsetX, offsetY, image=photo, anchor="nw")
    canvas1Practice.pack()
    canvastemp.pack()
    top.update()
    canvas1Practice.focus_set()
    canvas1Practice.bind("<Key>", waitConfirm)
    top.wait_variable(balance)
    canvasChangePic(imPractice, r'img/delay_recognition_location.png', w, h, 3,canvas1Practice)
    ####################
    # 延迟识别-位置
    ###################
    for _ in range(2):
        # 1.屏幕中央出现一个十字
        canvasChangePic(imPractice, r'img/1_16.png', w, h, 2,canvas1Practice)
        # 2. 随机出现四张图片
        rightInts = RandomShow(w, h, imPractice)
        # 3. 出现一次白屏和一次黑屏
        canvasChangePic(imPractice, './img/white.png', w, h, 0.1,canvas1Practice)
        canvasChangePic(imPractice, './img/black.png', w, h, 3,canvas1Practice)
        # 4. 测试阶段
        canvas.pack()
        canvas.focus_set()
        TestDelayPosition(w, h, imPractice, rightInts,canvas1Practice)

    top.mainloop()


def Entrance(info: str):
    # global root1Master
    root1Master = Tk()
    root1Master.title(info)
    root1Master.geometry('500x250')
    root1Master.resizable(0, 0)
    frameMaster = Frame(root1Master, width=100, height=20).pack()
    label = Label(frameMaster, height=2,width = 30,text = info,font=("黑体",20))
    label.pack()
    button1master = Button(frameMaster, text="开始检测", width=30, height=4, command=Step1)
    button1master.pack()
    button2master = Button(frameMaster, text="开始练习", width=30, height=4, command=Step1Practice)
    button2master.pack()
    root1Master.mainloop()


def main():
    root = Tk()
    root.title("DMS测试系统")
    root.geometry('500x250')
    # root.resizable(0, 0)
    frame = Frame(root, width=100, height=20).pack()
    button1 = Button(frame, text="延迟识别-位置", width=30, height=4, command=lambda: Entrance(info='延迟识别-位置')).pack()
    button2 = Button(frame, text="延迟识别-语言", width=30, height=4).pack()
    button3 = Button(frame, text="延迟回忆-位置", width=30, height=4).pack()

    root.mainloop()


if __name__ == '__main__':
    # RandomShow()
    # main()
    # Step1()
    Entrance("延迟识别-位置")
