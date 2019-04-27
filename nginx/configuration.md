### nginx配置

2019-4-26



#### 安装及测试配置文件，查看版本

```shell
$ sudo apt-get install nginx
$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
$ nginx -v
nginx version: nginx/1.14.0 (Ubuntu)
```



#### nginx.conf

```conf
#指定nginx进程运行时使用的用户
user www-data;

#设定worker process的数量
worker_processes auto;


```

#### 添加对PHP的支持



#### 虚拟主机的设置



#### 给站点启用SL



#### 反向代理设置

