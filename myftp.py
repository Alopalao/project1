import socket
import subprocess

request = ''
response = ''
command = ''
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#mysocket.connect(('inet.cs.fiu.edu', 21))
mysocket.connect(('inet.cs.fiu.edu', 21))
response = bytes.decode(mysocket.recv(1024))
print(response)
command = input ('USER: ')
request = 'User ' + command + '\n'
mysocket.send(str.encode(request))
response = bytes.decode(mysocket.recv(1024))
print(response)
command = input('Password: ')
request = 'Pass ' + command + '\n'
mysocket.send(str.encode(request))
response = bytes.decode(mysocket.recv(1024))
print(response)
#while(command != 'quit'):
command = input('myftp> ')
request = 'PASV\r\n'
mysocket.send(str.encode(request))
response = bytes.decode(mysocket.recv(1024))
print(response)

word = 0
number1 = ''
number2 = ''
for i in response:
    if(i == ','):
        word += 1
    elif(i == ')'):
        break
    elif(word == 4):
        number1 += i
    elif(word == 5):
        number2 += i

print("Number 1: ", number1)
print("number 2: ", number2)
total = int((int(number1)*256)+int(number2))
print("Total = ", total)

mysocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysocket2.connect(('inet.cs.fiu.edu', total))

request = 'NLST\r\n'
mysocket.send(str.encode(request))
response = bytes.decode(mysocket2.recv(1024))
print(response)

mysocket.send(str.encode('quit'))


mysocket.close()