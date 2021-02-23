import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('localhost', 1010))

s.send(b'5')

buffer = []
# 每次最多接收1k字节:
d = s.recv(1024)
# buffer.append(d)
# data = b''.join(buffer)
# print(data)
s.close()