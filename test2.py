# 延迟识别-言语
from tkinter import *
import config
from utils import *
from tkinter.messagebox import showinfo,askyesno
import random

balance = None
balanceShow = None
canvas = None
GroundTrue = True
root = None
root1 = None
root2 = None
root3 = None
root4 = None
MaxWidth = 0
MaxHeight = 0


def canvasChangePic(im, path, w, h, t):
    photo = loadPic(path, w, h)
    canvas.itemconfigure(im, image=photo)
    canvas.pack()
    root1.update()
    time.sleep(t)


def RandomShow(w, h, im):
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
        currentInt = random.randint(0,9)
        if currentInt != lastInt:
            randInts.append(currentInt)
            lastInt = currentInt
        if len(randInts)==4:
            break
    randPaths = ['./src/test2/' + str(x) + '.png' for x in randInts]
    for path in randPaths: canvasChangePic(im, path, w, h, 1)
    print(randInts)
    return randInts

def TestDelayPosition(w,h,im,rightInt):
    """
    测试延迟识别-位置
    :param w: 图片的宽度
    :param h: 图片的高度
    :param im: canvas图像对象
    :param rightInt: 正确图片位置数组
    :return:
    """
    global GroundTrue
    randInts,TrueIndex = creatTestDataset(rightInt,total_num=10)
    randPaths = ['./src/test2/' + str(x) + '.png' for x in randInts]
    for i,path in enumerate(randPaths):
        canvasChangePic(im, path, w, h, 1)
        if i == TrueIndex:
            GroundTrue = True
        else:
            GroundTrue = False
        canvas.wait_variable(balance)
    print(randInts)
    return randInts

def waitSpace(event):
    global balance
    print("字符：",event.char)

def waitConfirm(event):
    global balance
    global GroundTrue
    global balanceShow
    if event.char == ' ':
        balance = IntVar(root1,1,name = "balance")
        balanceShow = 1
        return
    if event.char in ['m','c']:
        if balanceShow==0:
            balance = IntVar(root1,1,name = "balance")
            balanceShow = 1
        elif balanceShow == 1:
            balance = IntVar(root1, 0, name="balance")
            balanceShow = 0
        if (event.char == 'm' and GroundTrue == True) or (event.char == 'c' and GroundTrue == False):
            pass
        else:
            pass


def Step1():
    global canvas
    global root1
    global balance
    global balanceShow
    # root1 = Toplevel()
    root1 = Tk()
    balance = IntVar(root1,0,name = "balance")
    balanceShow = 0
    MaxWidth = root1.winfo_screenwidth() # 设置窗口最大宽度为屏幕宽度
    MaxHeight = root1.winfo_screenheight() - 10
    root1.title("DMS测试")
    root1.resizable(0, 0)
    canvas = Canvas(root1, width=MaxWidth, height=MaxHeight, bg='black')
    photo = loadPic(r'./src/globle/start.png',MaxHeight,MaxHeight)
    offsetX = (MaxWidth - MaxHeight) / 2
    offsetY = 0
    im = canvas.create_image(offsetX, offsetY, image=photo, anchor="nw")
    canvas.pack()
    root1.update()
    canvas.focus_set()
    canvas.bind("<Key>",waitConfirm)
    root1.wait_variable(balance)
    # 给出测试提示
    canvasChangePic(im,r'./src/test2/delay_recognition_number.png',MaxHeight,MaxHeight,3)
    ####################
    # 延迟识别-位置
    ###################
    for _ in range(20):
        # 1.屏幕中央出现一个十字
        canvasChangePic(im,r'./src/globle/1_5.png',MaxHeight,MaxHeight,2)
        # 2. 随机出现四张图片
        rightInts = RandomShow(MaxWidth, MaxHeight, im)
        # 3. 出现一次白屏和一次黑屏
        canvasChangePic(im, './src/globle/white.png', MaxWidth, MaxHeight, 0.1)
        canvasChangePic(im, './src/globle/black.png', MaxWidth, MaxHeight, 3)
        # 4. 测试阶段
        canvas.pack()
        canvas.focus_set()
        # showinfo("提示","屏幕中央会随机出现9个图形中的任一个图形\n请您判断当前出现的图形和前一个出现的图形是否相同?\n"
        #               "如果相同，请按键盘【M】键;\n如果不同，请按键盘【C】键\n要求反映又快有对")
        TestDelayPosition(MaxWidth,MaxHeight,im,rightInts)
    root1.mainloop()

def main():
    global root
    root = Tk()
    root.title("DMS测试系统")
    root.geometry('500x250')
    root.resizable(0,0)
    # MaxWidth = root.winfo_screenwidth() # 设置窗口最大宽度为屏幕宽度
    # MaxHeight = root.winfo_screenheight() - 10
    frame = Frame(root,width = 100,height = 20).pack()
    button1 = Button(frame,text = "延迟识别-位置",width = 30,height = 3,command = Step1).pack()
    button2 = Button(frame,text = "延迟识别-语言",width = 30,height = 3).pack()
    button3 = Button(frame,text = "延迟回忆-位置",width = 30,height = 3).pack()
    button4 = Button(frame,text = "练习程序",width = 30,height = 3).pack()

    root.mainloop()


if __name__ == '__main__':
    Step1()
