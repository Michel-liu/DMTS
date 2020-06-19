from tkinter import *

class DMS():
    root = Tk()
    MaxWidth = 1000
    MaxHeight = 1000
    row = 4
    column = 4
    def __init__(self):
        self.CreateFrame()
        self.CreateGrid()

    def CreateFrame(self):
        self.root.title("DMS测试")
        self.root.geometry(str(self.MaxWidth)+"x"+str(self.MaxHeight))
        self.root.resizable(0,0)
    def CreateGrid(self):
        for i in range(self.row * self.column):
            row = i // self.row + 1
            col = i % self.row + 1
            frame = Frame(self.root,height = 25,width = 25).grid(row = row,column = col)
            Button(frame,text = "hell world").grid(row = 1,column = 1)
        row_count,column_count = self.root.grid_size()
        for row in range(1,row_count+1):
            self.root.grid_rowconfigure(row,minsize = 0)
        for col in range(1,column_count+1):
            self.root.grid_columnconfigure(col,minsize = 0)



    def Show(self):
        self.root.mainloop()

dms = DMS()
dms.Show()
