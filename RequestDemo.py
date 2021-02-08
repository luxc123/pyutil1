import json
import requests
import xlwt


def write_excel(titleResultDict, titleUrlDict):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('执行报告', cell_overwrite_ok=True)
    row0 = ["模块", "执行结果", "报告"]
    # 写第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    a = 0
    for i in titleResultDict:
        # print(i, ':', titleResultDict[i], '报告:', titleUrlDict[i])
        sheet1.write(a + 1, 0, i, set_style('Times New Roman', 220, False))
        sheet1.write(a + 1, 1, titleResultDict[i], set_style('Times New Roman', 220, False))
        sheet1.write(a + 1, 2, titleUrlDict[i], set_style('Times New Roman', 220, False))
        a = a + 1
    f.save('D:/用例报告.xls')

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

ipUrl = 'http://10.8.202.194:8080/{}'
loginUrl = ipUrl.format('login')
dataListUrl = ipUrl.format("api/case_manager")
testUrl = ipUrl.format('api/execute_cases/')

# 登录获取token
re = requests.post(loginUrl, json={"username": "yangtao167", "password": "a123456", "remeberPw": "on"})
data = re.text
print(data.encode('utf-8').decode('unicode_escape'))
cook = re.cookies._cookies
# print(cook)
cookObj = cook['10.8.202.194']['/']['sessionid']
# print(cookObj.value)

# 获取用例列表信息
dataRe = requests.post(dataListUrl, json={
    "type": "tree",
    "subsystem_id": "34",
    "module_id": "",
    "case_id": ""
}, headers={"cookie": "sessionid=" + cookObj.value}
                       )
dateResp = dataRe.text.encode('utf-8').decode('unicode_escape')
# print(dateResp)

listObj = json.loads(dateResp)
childrenList = listObj['data'][0]['children']

idTitleDict = {}
for index in range(len(childrenList)):
    # print(childrenList[index]['title'])
    idTitleDict[childrenList[index]['id']] = [childrenList[index]['title']]

titleResultDict = {}
titleUrlDict = {}
for index in range(len(childrenList)):
    # if index > 5:
    #     break
    id = childrenList[index]['id']
    # 不调用测试人员接口
    if id == 1664 or id == 1719:
        continue
    # print(idTitleDict[id][0])
    url = 'http://10.8.202.194:8080/api/execute_cases/{}'.format(id)
    testRe = requests.post(url, headers={"cookie": "sessionid=" + cookObj.value})
    restStr = testRe.text.encode('utf-8').decode('unicode_escape')
    restObj = json.loads(restStr)
    if restObj['code'] != 404:
        titleResultDict[idTitleDict[id][0]] = restObj['message']
        titleUrlDict[idTitleDict[id][0]] = ipUrl.format(restObj['report_path']).replace('//', '/')
        print(idTitleDict[id][0], ':', restObj['message'])

print('>>>>>>>>>>>>>>>>>>>>>>报告<<<<<<<<<<<<<<<<<<<<<<<<')
# for i in titleResultDict:
#     print(i, ':', titleResultDict[i], '报告:', titleUrlDict[i])

print('已生成---D:/用例报告.xls ,请查看')
write_excel(titleResultDict, titleUrlDict)
input('Press Any Key')