#!/usr/bin/python3
#coding: utf8

def 简单替换(加密内容):
    明文字母表 = "abcdefghijklmnopqrstuvwxyz"
    密文字母表 = "phqgiumeaylnofdxjkrcvstzwb"

    密文 = ""
    for 字符 in 加密内容:
        if 字符 in 明文字母表:
            密文 += 密文字母表[明文字母表.find(字符)]
        else:
            密文 += 字符
    return 密文

print(简单替换("the quick brown fox jumps over the lazy dog"))