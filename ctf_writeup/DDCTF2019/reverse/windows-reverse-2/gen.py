#!/usr/bin/python3
#coding: utf8
from base64 import *

flag_base64ed = "reverse+"

bin_input = b64decode(flag_base64ed.encode("ascii"))
flag = ""
for i in bin_input:
	flag+=hex(i)[2:].upper()

print("DDCTF{%s}" % flag)

