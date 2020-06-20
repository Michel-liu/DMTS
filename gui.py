from tkinter import *
from PIL import ImageTk,Image
import config

def callback(event):
    print(config.Height)
    return (event.x, event.y)

class DMS():
    def __init__(self):
        self.root = Tk()
        self.MaxWidth = self.root.winfo_screenheight()
        self.MaxHeight = self.root.winfo_screenheight()
        config.Height = self.MaxHeight
        self.root.title("DMS测试")
        self.frame = Frame(self.root,height = self.MaxHeight,width = self.MaxWidth)
        self.root.resizable(0,0)
        self.ClickEvent()

    def ClickEvent(self):
        self.frame.bind("<Button-1>",callback)
        self.frame.pack()
    def Show(self):
        self.root.mainloop()

dms = DMS()
dms.Show()
