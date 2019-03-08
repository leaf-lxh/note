# 知识储备  
## 基础  
- [x] PHP易产生漏洞的函数，易产生漏洞的php.ini配置项  
- [ ] 对于SQL注入，PHP的一些字符过滤函数，以及参数化查询的写法  （sqllib）  
- [ ] 对于XSS，CSRF，PHP的实体转义函数htmlspecialchars()使用  （自搭环境）  
- [x] 文件包含，PHP伪协议  （自搭环境）  
- [ ] 文件上传，后缀名绕过，MIME类型绕过  （uploadlib）  

## 一阶段   
- [ ] 日志系统，WAF的配置  

## 二阶段  
- [x] 利用python scapy库发包      
- [ ] 生成树协议、ARP协议、DHCP协议、路由协议、TCP协议的安全隐患，利用方式，修补或限制的方式。  （交换机上的配置） 
- [ ] jpg，png，gif图片隐写  
- [ ] 古典密码  
- [ ] flask模板漏洞  

## 三阶段  
- [x] PHP高危函数禁用，以及利用反射函数进行绕过
- [x] vsftpd的匿名用户，目录穿越, rlogind弱口令修补配置  
- [ ] MySQL，SQLserver账户密码修改，监听端口修改  
- [x] webshell，内存马查找  
- [ ] PAM模块配置  
- [x] 权限维持  
- [ ] kali工具（爆破zip文件，爆破系统账号口令，searchsploit提权exp）  
- [x] iptables封堵端口  
- [x] pwn

___
# Python脚本准备  
- [x] 自写arpspoof，分别利用Python的scapy库和rawsocket实现  
- [x] 自动修改系统账户密码脚本  
- [ ] web访问分析（包括其他队伍访问的url,文件上传目录的实时监控与抄袭）  
- [ ] 缺陷服务的自动化扫描（ssh弱口令登录  
- [x] base全家桶，AES，DES，哈希函数全家桶使用脚本  
- [x] 敏感函数扫描脚本 /workspace/code/python/scan_tool/main.py  
# 权限维持  

- [ ] C++ , nc, perl 反弹shell  
- [ ] 隐藏进程  

# 思路  

Linux:

修改系统账户、数据库弱口令

vsftpd 禁用anonymous账户登录，启用用户白名单

sshd 禁用空密码登录、禁止root登录

rlogind 禁止免密码登录


