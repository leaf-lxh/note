## Linux ELF保护措施

### NX（no execute)

使得栈上的数据不可执行

使用`readelf`命令查看是否开启了此项保护措施

```shell
$ readelf -l babyheap 

Elf 文件类型为 DYN (共享目标文件)
入口点 0xad0
共有 9 个程序头，开始于偏移量 64

程序头：
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000000040 0x0000000000000040
                 0x00000000000001f8 0x00000000000001f8  R E    8
  INTERP         0x0000000000000238 0x0000000000000238 0x0000000000000238
                 0x000000000000001c 0x000000000000001c  R      1
      [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x000000000000183c 0x000000000000183c  R E    200000
  LOAD           0x0000000000001d60 0x0000000000201d60 0x0000000000201d60
                 0x0000000000000380 0x00000000000003b8  RW     200000
  DYNAMIC        0x0000000000001d78 0x0000000000201d78 0x0000000000201d78
                 0x00000000000001c0 0x00000000000001c0  RW     8
  NOTE           0x0000000000000254 0x0000000000000254 0x0000000000000254
                 0x0000000000000044 0x0000000000000044  R      4
  GNU_EH_FRAME   0x00000000000015a0 0x00000000000015a0 0x00000000000015a0
                 0x000000000000007c 0x000000000000007c  R      4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     10
  GNU_RELRO      0x0000000000001d60 0x0000000000201d60 0x0000000000201d60
                 0x00000000000002a0 0x00000000000002a0  R      1

```

如果GNU_STACK项不存在或GNU_STACK 项有X属性，则没有开启NX

### PIE（position independent executable）

使程序运行时的入口地址随机

使用`readelf`命令查看是否开启了此项保护措施

```shell
$ readelf -h babyheap 
ELF 头：
  Magic：   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  类别:                              ELF64
  数据:                              2 补码，小端序 (little endian)
  版本:                              1 (current)
  OS/ABI:                            UNIX - System V
  ABI 版本:                          0
  类型:                              DYN (共享目标文件)
  系统架构:                          Advanced Micro Devices X86-64
  版本:                              0x1
  入口点地址：               0xad0
  程序头起点：          64 (bytes into file)
  Start of section headers:          12032 (bytes into file)
  标志：             0x0
  本头的大小：       64 (字节)
  程序头大小：       56 (字节)
  Number of program headers:         9
  节头大小：         64 (字节)
  节头数量：         29
  字符串表索引节头： 26

```

结果中入口点地址如果为一个很小的值（只有偏移值）则说明开启了此保护

### ASLR（Address Space Layout Random）

摘自<https://blog.51cto.com/duallay/1876841>

Linux下的ASLR总共有3个级别，0、1、2

- 0:0就是关闭ASLR，没有随机化，堆栈基地址每次都相同，而且libc.so每次的地址也相同。

- 1:1是普通的ASLR。mmap基地址、栈基地址、.so加载基地址都将被随机化，但是堆没用随机化

- 2:2是增强的ASLR，增加了堆随机化（等同于brk随机？）

  

```
查询randomize_va_space当前设置:
# sysctl -n kernel.randomize_va_space
1

//这就是个文件，里面记录着等级
# cat /proc/sys/kernel/randomize_va_space
1

```



```
关闭ASLR:

# sysctl -w kernel.randomize_va_space=0

# echo 0 > /proc/sys/kernel/randomize_va_space
```

### Stack Canary

在栈上的返回地址的前面放置一个cookie，在结束函数执行时，会检测此cookie，如果cookie值被篡改则直接报错，使得栈溢出无法修改cookie后面的内容。

通过查看汇编代码，如果函数的开头将fs:0x28的值放置到栈返回地址的前面，则开启了stack canary