# 系统运维从修补到宕机
3-6

## 目录
正在建设中
___

## Linux 服务

### openssh-server
提供ssh服务  
配置文件：
/etc/ssh/sshd_conf  
加固：修改配置文件
```conf
#设定端口，默认端口22
Port 22

#是否允许root用户远程登录
#可选3个值：
#   yes:允许远程登录
#   no:不允许远程登录
#   prohibit-password:禁止使用密码登录
PermitRootLogin no 

#是否允许RSA验证 yes/no
RSAAuthentication yes
PubkeyAuthentication yes

#是否允许使用密码登录 yes/no
PasswordAuthentication no

#是否允许使用空密码登录 yes/no
PermitEmptyPasswords no

#设定使用的syslog设施，日志文件名称在/etc/rsyslog.d/50-default.conf有设定
#(旧版本的rsyslog名称为syslog,配置文件在/etc/syslog.conf)
#auth,authpriv.*                 /var/log/auth.log
SyslogFacility AUTHPRIV

```

### vsftpd
提供ftp服务  
配置文件：/etc/vsftpd.conf  
加固：修改配置文件， v2.3.4版本还需封堵后门  
```conf
#是否允许匿名登录  YES/NO
anonymous_enable=NO #不允许

#是否允许本地用户登录 YES/NO
local_enable=YES

#是否允许写操作 YES/NO
write_enable=YES

#是否允许匿名用户写入文件 YES/NO
anon_upload_enable=NO

#是否允许匿名用户创建目录 YES/NO
non_mkdir_write_enable=NO

#设定日志位置
xferlog_file=/var/log/vsftpd.log

#设定禁止用户走出自己的根目录
chroot_local_user=YES
chroot_list_enable=NO

#设定使用用户列表，以及指定用户列表位置
#用户列表中存放可登录ftp服务的用户，每个用户用换行符隔开
userlist_enable=YES
userlist_deny=NO  #是否使用黑名单机制 YES/NO
userlist_file=/etc/vsftpd.userlist
```

关于v2.3.4笑脸后门：  
通过使用任意账户名加上:)作为账号登录，密码任意，vsftpd会在6200TCP端口上映射一个shell  
封堵方法有两个，一个是通过使用用户列表，使用用户列表白名单后后门不会被触发，另一个是通过iptables规则禁止后门连接
```
220 (vsFTPd 2.3.4)
Name (192.168.247.250:leaf): niconiconi:)
331 Please specify the password.
Password:


iptables -I 
```

