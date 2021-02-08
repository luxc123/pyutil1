import os

list = []
f = open("D:\启动文件.txt", 'r', encoding='UTF-8')
line = f.readline()
while line:
    list.append(line.replace('\n',''))
    line = f.readline()
f.close()

for index in range(len(list)):
    os.startfile(list[index])


