# 古典密码
19-02-25

引用以及参考：  
[https://ctf-wiki.github.io/ctf-wiki/crypto/classical/monoalphabetic/](https://ctf-wiki.github.io/ctf-wiki/crypto/classical/monoalphabetic/)  
___
## 目录
* [单表代换加密](#1)
    * [凯撒密码](#1.1)
    * [移位密码](#1.2)
    * [简单替换密码](#1.3)
    * [埃特巴什(Atbash)码](#1.4)
    * [仿射密码](#1.5)
* [多表代换加密](#2)
    
* [其他类型的加密算法](#3)
    * [培根密码](#2.1)

___

## <font id="1" >单表代换加密</font>
单表代换加密有一个特点，就是明文和密文之间有一个**对应关系**。   
明文根据密码表进行转换===》得到密文

### <font id="1.1">凯撒密码</font>
凯撒密码是**将明文中的`字母`按照字母表进行偏移**，得到密文。**偏移量**称为密钥。  
如果题目中只有字母发生了变换，则要考虑是不是凯撒密码。   
可以尝试暴力破解，26种可能中一般总会有正确的明文  

举个栗子：

>明文字母表：ABCDEFGHIJKLMNOPQRSTUVWXYZ  
>偏移量为3，方向向右  
>密文字母表：DEFGHIJKLMNOPQRSTUVWXYZABC
>
>明文： THIS IS AN ENCRYPTED MESSAGE  
>密文： WKLV LV DQ HQFUBSWHG PHVVDJH  


>一些特定偏移量的凯撒密码有自己的名称  
>偏移量为 10：Avocat （A→K）  
>偏移量为 13：ROT13  
>偏移量为 -5：Cassis （K 6）  
>偏移量为 -6：Cassette （K 7）  
>**其中由于ROT13的偏移量为13，正好是半个周期，所以其密文再次经过加密算法加密后会变成明文。  
>另外php有函数可以进行rot13加密，函数名为str_rot13()**

>此外，还有还有一种基于密钥的凯撒密码 Keyed Caesar。其基本原理是 利用一个密钥，将密钥的每一位转换为数字（一般转化为字母表对应顺序的数字），分别以这一数字为密钥加密明文的每一位字母。  
>
>这里以 XMan 一期夏令营分享赛宫保鸡丁队 Crypto 100 为例进行介绍。
```
密文：s0a6u3u1s0bv1a
密钥：guangtou
秘钥对应的每一位偏移：6,20,0,13,6,19,14,20
明文：y0u6u3h1y0uj1u
```
### <font id="1.2">移位密码</font>
>与凯撒密码类似，区别在于移位密码不仅会处理字母，还会处理数字和特殊字符，常用 ASCII 码表进行移位。  
>其破解方法也是遍历所有的可能性来得到可能的结果。

### <font id="1.3">简单替换密码</font>
简单替换密码与凯撒密码类似，都要有个对应关系，根据对应关系将明文转换成密文。
凯撒密码是根据偏移来生成密码表（也就是对应关系）。与凯撒密码不同的是，简单替换密码的密码表是无规律生成的，所以爆破起来就很费劲。解密的话需要知道对应关系，或者进行词频分析。
举个粒子：
>明文字母 : abcdefghijklmnopqrstuvwxyz   
>密钥字母 : phqgiumeaylnofdxjkrcvstzwb   
>   
>明文：the quick brown fox jumps over the lazy dog   
>密文：cei jvaql hkdtf udz yvoxr dsik cei npbw gdm   

python脚本实现：

```python
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
```
### <font id="1.4">埃特巴什(Atbash)码</font>
埃特巴什码是上面简单替换的一个特例，对应关系不是无规则的。   
对应关系为：使用字母表中的最后一个字母代表第一个字母，倒数第二个字母代表第二个字母。以此类推   

>明文：A B C D E F G H I J K L M N O P Q R S T U V W X Y Z   
>密文：Z Y X W V U T S R Q P O N M L K J I H G F E D C B A

举个梨子：
>明文：the quick brown fox jumps over the lazy dog   
>密文：gsv jfrxp yildm ulc qfnkh levi gsv ozab wlt

### <font id="1.4">仿射密码</font>
挖坑待续....
___
## <font id="2">多表代换加密</font>
如果想破解的话，有兴趣可以去搜搜资料....[ctf-wiki](https://ctf-wiki.github.io/ctf-wiki/crypto/classical/polyalphabetic/)
这里只写一下加密与解密过程   

### <font id="2.1">Playfair</font>
>Playfair 密码（Playfair cipher or Playfair square）是一种替换密码，1854 年由英国人查尔斯 · 惠斯通（Charles Wheatstone）发明，基本算法如下：
> 1. 选取一串英文字母，除去重复出现的字母，将剩下的字母逐个逐个加入 5 × 5 的矩阵内，剩下的空间由未加入的英文字母依 a-z 的顺序加入。注意，将 q 去除，或将 i 和 j 视作同一字。  
> 2. 将要加密的明文分成两个一组。若组内的字母相同，将 X（或 Q）加到该组的第一个字母后，重新分组。若剩下一个字，也加入 X 。  
> 3. 在每组中，找出两个字母在矩阵中的地方。  
>> * 若两个字母不同行也不同列，在矩阵中找出另外两个字母（第一个字母对应行优先），使这四个字母成为一个长方形的四个角。  
>> * 若两个字母同行，取这两个字母右方的字母（若字母在最右方则取最左方的字母）。  
>> * 若两个字母同列，取这两个字母下方的字母（若字母在最下方则取最上方的字母）。  
>> * 新找到的两个字母就是原本的两个字母加密的结果。  


