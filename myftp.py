import socket
import shutil
import sys

def Pasv_mode():
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
    Port = int((int(number1)*256)+int(number2))
    mysocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket2.connect((sys.argv[1], Port))
    return mysocket2

def command_ls(mysocket, argument2):
    if(len(argument2) > 0):
        request = 'CWD ' + argument2 + '\r\n'
        mysocket.send(str.encode(request))
        response = bytes.decode(mysocket.recv(1024))
    mysocket2 = Pasv_mode()
    request = 'NLST\r\n'
    mysocket.send(str.encode(request))
    response = bytes.decode(mysocket.recv(1024))
    print(response)
    response = bytes.decode(mysocket2.recv(1024))
    print(response)
    response = bytes.decode(mysocket.recv(1024))
    print(response)
    if(len(argument2) > 0):
        request = 'CWD ..\r\n'
        mysocket.send(str.encode(request))
        response = bytes.decode(mysocket.recv(1024))
    
def command_cd(mysocket, argument2):
    request = 'CWD ' + argument2 + '\r\n'
    mysocket.send(str.encode(request))
    response = bytes.decode(mysocket.recv(1024))
    print(response)

def command_get(mysocket, argument2):
    mysocket2 = Pasv_mode()
    request = 'RETR ' + argument2 + '\r\n'
    mysocket.send(str.encode(request))
    response = bytes.decode(mysocket.recv(1024))
    print(response)
    file_got = open(argument2, 'wb')
    file_recv = mysocket2.recv(1024)
    file_got.write(file_recv)
    print("The file's size is " + str(len(file_recv)) + " bytes")
    response = bytes.decode(mysocket.recv(1024))
    print(response)
    
def command_put(mysocket2, argument2):
    mysocket2 = Pasv_mode()
    request = 'STOR ' + argument2 + '\r\n'
    mysocket.send(str.encode(request))
    response = bytes.decode(mysocket.recv(1024))
    print(response)
    file_sent = open(argument2, 'rb')
    file_arrive = file_sent.read()
    print("The file's size is " + str(len(file_arrive)) + " bytes")
    mysocket2.send(file_arrive)

def command_delete(mysocket2, argument2):
    request = 'DELE ' + argument2 + '\r\n'
    mysocket.send(str.encode(request))
    response = bytes.decode(mysocket.recv(1024))
    print(response)

name_server = sys.argv[1]
request = ''
response = ''
command = ''
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysocket.connect((sys.argv[1], 21))
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

count = 0
for q in response:
    if(q == 'u'):
        count += 1

if(count != 2):
    print('Quitting the server')
    command = 'quit'

while(command != 'quit'):
    command = input('myftp> ')
    argument1 = ''
    argument2 = ''
    word = 0
    for i in command:
        if(i == ' '):
            word += 1
        elif(word == 1):
            argument2 += i
        elif(word == 0):
            argument1 += i

    if(argument1 == 'ls'):
        command_ls(mysocket, argument2)
    elif(argument1 == 'cd'):
        command_cd(mysocket, argument2)
    elif(argument1 == 'get'):
        command_get(mysocket, argument2)
    elif(argument1 == 'put'):
        command_put(mysocket, argument2)
        response = bytes.decode(mysocket.recv(1024))
        print(response)
    elif(argument1 == 'delete'):
        command_delete(mysocket, argument2)
    elif(argument1 == 'quit'):
        mysocket.send(str.encode('quit'))
    else:
        print('The command "' + argument1 + '" is unknown')

mysocket.close()