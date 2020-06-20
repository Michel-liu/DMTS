from tkinter import *
from PIL import ImageTk, Image
from config import *
import time
from utils import *



def main():
    root = Tk()
    MaxWidth = root.winfo_screenheight()  # 设置窗口最大宽度为屏幕宽度
    MaxHeight = root.winfo_screenheight()
    config.Height = MaxHeight  # 将配置文件中窗口宽度设置为屏幕宽度
    root.title("DMS测试")
    frame = Frame(root, width=MaxWidth, height=MaxHeight)
    frame.pack()
    photo = loadPic(r'./img/test.png', MaxHeight, MaxWidth)
    imgLabel1 = Label(frame, image=photo, width=MaxWidth, height=MaxHeight)  # 把图片整合到标签类中
    imgLabel1.bind("<Return>", handlerAdaptor(callback,path = "./img/1_16.png",maxw = MaxWidth,maxh = MaxHeight))
    imgLabel1.pack()
    #######################
    # 第一阶段，十字出现500ms
    #######################
    # time.sleep(0.5)
    #######################
    # 第二阶段，随机位置白色圆图片出现各一秒
    #######################
    # 1. 第一个图片
    photo = loadPic(r'./img/4.png', MaxWidth, MaxHeight)
    imgLabel1.configure(image=photo)
    # time.sleep(1)
    # 2. 第二个图片
    photo = loadPic(r'./img/7.png', MaxWidth, MaxHeight)
    imgLabel1.configure(image=photo)
    # time.sleep(1)
    #
    imgLabel2 = Label(frame, image=photo, width=MaxWidth, height=MaxHeight)  # 把图片整合到标签类中

    imgLabel2.bind("<Button-1>", handlerAdaptor(callback, path=r'./img/white.png', maxw=MaxWidth, maxh=MaxHeight))
    # imgLabel2.pack()  # 自动对齐
    root.mainloop()


if __name__ == '__main__':
    main()
