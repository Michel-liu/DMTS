from tkinter import *
from PIL import ImageTk,Image
import config
from utils import *


class DMS():
    """
    gui 主窗口类
    """
    def __init__(self):
        """
        gui窗口类初始化
        """
        self.root = Tk()
        self.MaxWidth = self.root.winfo_screenheight()      # 设置窗口最大宽度为屏幕宽度
        self.MaxHeight = self.root.winfo_screenheight()
        config.Height = self.MaxHeight                      # 将配置文件中窗口宽度设置为屏幕宽度
        self.root.title("DMS测试")
        self.frame = Canvas(self.root,height = self.MaxHeight,width = self.MaxWidth,bd=0,highlightthickness=0)
        self.root.resizable(0,0)                            # 设置窗口大小不可变
        self.ClickEvent()
        self.SetBackGround()

    def ClickEvent(self):
        """
        将窗口绑定鼠标左键点击事件
        :return:
        """
        self.frame.bind("<Button-1>",callback)
        self.frame.pack()

    def SetBackGround(self,path = "./1.gif"):
        photo = PhotoImage(file = path)
        self.label = Label(self.root,image = photo)
        self.label.pack()
    def Show(self):
        self.root.mainloop()

    def Run(self):
        self.SetBackGround()


dms = DMS()
dms.Show()
