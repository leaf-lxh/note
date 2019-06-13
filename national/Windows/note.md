

### 信息收集

systeminfo 查看系统信息

hostname 查看主机名

route print打印路由表

arp -a 查看所有的ARP表

ipconfig /displaydns  查看最近解析的DNS

netsh firewall show state 查看防火墙状态

netsh firewall show config查看防火墙配置

net start 查看启动的服务

DRIVERQUERY 查看安装的驱动程序

dir /s 搜索文件

tasklist /SVC  查看进程

wmic 命令

*accesschk 查看每一个服务的权限*

net start upnphost





wmic qfe get Caption,Description,HotFixID,InstalledOn 查看安装的补丁

开关远程桌面

wmic RDTOGGLE WHERE ServerName='%COMPUTERNAME%' call SetAllowTSConnections 1

wmic RDTOGGLE WHERE ServerName='%COMPUTERNAME%' call SetAllowTSConnections 0



查看计划任务，运行的程序，服务，VPN

端口隐藏

文件隐藏

进程隐藏

注册表隐藏

