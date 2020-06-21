from tkinter import *
import config
from utils import *
from tkinter.messagebox import showinfo
import random

canvas = None
root = None
MaxWidth = 0
MaxHeight = 0


def canvasChangePic(im, path, w, h, t):
    photo = loadPic(path, w, h)
    canvas.itemconfigure(im, image=photo)
    canvas.pack()
    root.update()
    time.sleep(t)


def RandomShow(w, h, im):
    """
    随机出现四张图片
    :param w: 图片的宽度
    :param h: 图片的高度
    :param im: canvas的图片对象
    :return: 正确的图片位置
    """
    randInts = [random.randint(0, 15) for _ in range(4)]
    randPaths = ['./img/' + str(x) + '.png' for x in randInts]
    for path in randPaths:
        canvasChangePic(im, path, w, h, 1)
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
    randInts = [random.randint(0, 15) for _ in range(20)]
    randPaths = ['./img/' + str(x) + '.png' for x in randInts]
    for path in randPaths:
        canvasChangePic(im, path, w, h, 1)
        print(path)
    return randInts



def main():
    global canvas
    global root
    root = Tk()
    log = Logger()
    MaxWidth = root.winfo_screenwidth() # 设置窗口最大宽度为屏幕宽度
    MaxHeight = root.winfo_screenheight()
    root.title("DMS测试")
    root.resizable(0, 0)
    canvas = Canvas(root, width=MaxWidth, height=MaxHeight, bg='black')
    ####################
    # 延迟识别-位置
    ###################
    # 1.屏幕中央出现一个十字
    photo = loadPic(r'./img/1_16.png', MaxHeight, MaxWidth)
    offsetX = (MaxWidth - MaxHeight) / 2
    offsetY = 0
    im = canvas.create_image(offsetX, offsetY, image=photo, anchor="nw")
    canvas.pack()
    root.update()
    time.sleep(0.5)
    # 2. 随机出现四张图片
    rightInts = RandomShow(MaxWidth, MaxHeight, im)
    # 3. 出现一次白屏和一次黑屏
    canvasChangePic(im, './img/white.png', MaxWidth, MaxHeight, 0.1)
    canvasChangePic(im, './img/black.png', MaxWidth, MaxHeight, 3)
    # 4. 测试阶段
    canvas.pack()
    canvas.focus_set()
    canvas.bind('<Key>',callback) # canvas 绑定键盘按键
    showinfo("提示","欢迎参加本次测试")
    TestDelayPosition(MaxWidth,MaxHeight,im,rightInts)

    root.mainloop()


if __name__ == '__main__':
    # RandomShow()
    main()
