# 知识点

2019-5-27

### Linux提权

- [x] [metasploit table2 内核漏洞提权](./Linux提权/metasploit_table2.md)
- [x] [MySQL UDF提权](./Linux提权/UDF利用.md)
- [ ] Linux系统命令

### Windows提权

- [ ] Windows server 2003 提权
- [ ] Windows server 2008 提权
- [ ] Windows XP 提权
- [ ] Windows信息收集用的命令


### Linux pwn

- [x] [Linux shellcode编写（gdb，readelf，objdump的使用）](./pwn/practices/xman-level1.md)
- [x] [Linux elf文件判断开启的保护措施](./pwn/checksec.md)
- [x] NX 绕过： ROP技术：ret2text/ret2plt/ret2libc/ret2dl-resolve
- [ ] 系统调用
- [x] [格式化字符串漏洞利用](./pwn/practice/cgfsb.md)
- [x] PIE绕过
- [x] Stack Canary绕过：[SSP](./pwn/practice/smashes.md)，劫持chk_fail函数
- [x] fastbin attack，UAF
- [x] unlink
- [ ] off one byte + unlink
- [ ] large bin attack
- [ ] house of 系列堆溢出利用

### Windows pwn

- [x] [Windows  硬编码shellcode](./pwn/windows_shellcode.md)
- [x] [利用PEB获取模块地址，实现与Windows版本无关的shellcode](./pwn/windows_shellcode.md)
- [ ] freefloat ftpserver实战
- [x] [CloudMe 从POC到EXP](./pwn/practices/cloudme.md)
- [ ] Windows常见反调试绕过

### 其他

- [x] [python端口扫描的三种方法实现：nmap，scapy，socket](./protocol/port_scan.md)
- [x] [python 使用scapy模块对arp协议进行利用](./protocol/arp.md)
- [x] python，c语言的socket编程
- [x] python argparse/optparse模块的使用
- [ ] [netcat基本使用](./pwn/netcat使用.md)
- [ ] 复习PHP常见漏洞
- [ ] 复习mysql注入
- [ ] mssql注入
- [ ] redis未授权访问漏洞
- [ ] jpg，png，gif图片隐写 
- [ ] xml实体注入漏洞
- [ ] Windows  server 2003，Windows server 2012 熟悉常用配置



### 最后十天

- [ ] 端口扫描，ARP利用的脚本多熟悉几遍
- [ ] Linux shellcode, Windows 硬编码shellcode再写几遍
- [ ] Windows ROP尝试做一下，云服务的题至少做一道，egg定位shellcode的原理搞懂
- [ ] 图片隐写，PHP复习，mysql从注入到getshell
- [ ] 由于三阶段的不可靠性，搭建mssql环境练习注入，熟悉Windows server加固