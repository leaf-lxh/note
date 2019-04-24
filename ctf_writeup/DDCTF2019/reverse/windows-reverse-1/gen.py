#!/usr/bin/python3
#coding: utf8
byte_list = []
for i in "DDCTF{reverseME}":
	byte_list.append(ord(i))

offset = []

for i in byte_list:
	offset.append(i - 0x20)

start = 0x403076
memory_address = []
for i in offset:
	#print(i)
	memory_address.append(start - i)

#for i in range(0, len(memory_address)):
	#print("%c : %x" %("DDCTF{reverseME}"[i], memory_address[i]))

for i in memory_address:
	print(chr(i-0x402FF8),end="")
