from tkinter import *
import config
from utils import *
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
    randInts = [random.randint(0, 15) for _ in range(4)]
    randPaths = ['./img/' + str(x) + '.png' for x in randInts]
    for path in randPaths:
        canvasChangePic(im, path, w, h, 1)
    print(randInts)
    return randInts


def main():
    global canvas
    global root
    root = Tk()
    log = Logger()
    MaxWidth = root.winfo_screenheight()  # 设置窗口最大宽度为屏幕宽度
    MaxHeight = root.winfo_screenheight()
    root.title("DMS测试")
    root.resizable(0, 0)
    canvas = Canvas(root, width=MaxWidth, height=MaxHeight, bg='black')
    ####################
    # 延迟识别-位置
    ###################
    # 1.屏幕中央出现一个十字
    photo = loadPic(r'./img/1_16.png', MaxHeight, MaxWidth)
    im = canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.pack()
    root.update()
    time.sleep(0.5)
    # 2. 随机出现四张图片
    RandomShow(MaxWidth, MaxHeight, im)
    # 3. 出现一次白屏和一次黑屏
    canvasChangePic(im, './img/white.png', MaxWidth, MaxHeight, 0.1)
    canvasChangePic(im, './img/black.png', MaxWidth, MaxHeight, 3)
    # 4. 测试阶段
    canvas.bind('<Key>',lambda event:canvas.focus_set(), callback)
    root.update()

    canvas.pack()
    root.mainloop()


if __name__ == '__main__':
    # RandomShow()
    main()
