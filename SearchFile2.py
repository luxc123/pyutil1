import os
import PIL
from PIL import Image
import tkinter
# from tkinter import *

def init(path):
    listdir = os.listdir(path)
    allfile = []
    dic = {}
    for file in listdir:
        absPath = path + '\\' + file
        dic[file] = absPath
        allfile.append(absPath)
    return dic



if __name__ == '__main__':

    root = tkinter.Tk()  # 创建窗口对象的背景色
    root.title('查找图片')
    root.geometry('500x300')  # 这里的乘是小x

    # 创建两个列表
    pathInput = tkinter.Entry(root, width='60')
    conditionInput = tkinter.Entry(root)
    button = tkinter.Button(root,  width='5', text="查询")

    def onclick(event):
        # fileDic = pathInput.get()
        condition = conditionInput.get()
        fileDic = init(pathInput.get())
        resultList = []
        for (k, v) in fileDic.items():
            if (condition in k):
                resultList.append(fileDic[k])
        for file in resultList:
            img = PIL.Image.open(file)
            img.show()

    conditionInput.bind('<Return>', onclick)
    button.bind("<Button-1>", onclick)

    label1 = tkinter.Label(root, text="文件夹路径")
    label2 = tkinter.Label(root, text="查询内容")

    label1.pack()  # 将小部件放置到主窗口中
    pathInput.pack()  # 将小部件放置到主窗口中
    label2.pack()  # 将小部件放置到主窗口中
    conditionInput.pack()  # 将小部件放置到主窗口中
    button.pack()  # 将小部件放置到主窗口中

    root.mainloop()  # 进入消息循环
