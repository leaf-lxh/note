此目录存放着关于逆向的练习笔记



由于有些题目是jarvis平台上的，因为不让把writeup放在网上，所以这个git仓库是非公开的



Windows7平台下，为了避免ASLR的影响，需要在注册表中修改（或添加）一项数值，关闭ASLR

方法为：

在**HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management**中，新建类型为DWORD的值，名称为**MoveImages**，数值为0，然后重启

Win7以上的平台暂未测试，Win XP及以下的版本默认没有开启ASLR

