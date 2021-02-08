import os
from PIL import Image
import json

jsonFileName = 'bunengchongfu.json'

# 获取文件夹下文件的绝对路径
def init(path):
    listdir = os.listdir(path)
    allfile = []
    dic = {}
    for file in listdir:
        absPath = path + '\\' + file
        dic[file] = absPath
        allfile.append(absPath)
    print(allfile)
    jsObj = json.dumps(dic,ensure_ascii=False,indent=4, separators=(',', ':'))
    fileObject = open(path+'\\'+jsonFileName, 'w', encoding='utf8')
    fileObject.write(jsObj)
    fileObject.close()
    return allfile

def init2(path):
    listdir = os.listdir(path)
    allfile = []
    dic = {}
    for file in listdir:
        absPath = path + '\\' + file
        dic[file] = absPath
        allfile.append(absPath)
    # print(allfile)
    # print(dic)
    return dic

# 打开图片
def getNameAndFilePathDic(allfile):
    for file in allfile:
        img = Image.open(file)
        img.show()

# 模糊搜索匹配的东西
def getAbleFile(condition,path):
    print("111")
    #先获取json文件符合的图片
    with open(path + '\\'+jsonFileName, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        print('这是文件中的json数据：', json_data)
        print('这是读取到文件数据的数据类型：', type(json_data))



if __name__ == '__main__':
    condition = input('请输入:')
    fileDic = init2(r'C:\Users\luxichao\Desktop\python - 副本')
    resultList = []
    for (k, v) in fileDic.items():
        if(condition in k):
            resultList.append(fileDic[k])
            print(k)
            print(fileDic[k])
    for file in resultList:
        img = Image.open(file)
        img.show()

        # print(allFile)
    # getNameAndFilePathDic(allFile)
    # getAbleFile("11",r'C:\Users\luxichao\Desktop\python - 副本')

