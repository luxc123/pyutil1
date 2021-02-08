import mysql.connector

# 10.8.203.187:3306/sub_contract?useUnicode=true&characterEncoding=utf-8&autoReconnect=true&serverTimezone=Asia/Shanghai
conn = mysql.connector.connect(user='root', password='Robot123!@#', host='10.8.203.187',port='3306',database='sub_contract')
cursor = conn.cursor()

cursor.execute('desc {}'.format('tender_qa'))
# cursor.execute('desc tender_qa')
values = cursor.fetchall()
print(values)


cursor.close()
conn.close()
