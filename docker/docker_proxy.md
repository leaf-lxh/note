## 给docker设置socks5代理

2019-5-13

由于内网的条件限制，一个账号只能登录一台设备。而现在有两台设备需要上网，于是在能上网的电脑上开启sock5代理，另一台设备通过这个代理上网。



一般来讲在不能上网的电脑上装一个proxychains就可解决（没网的情况下趁电脑不注意给它装上）

不过不知为何docker不能用proxychains来挂代理。



网上搜了一下，以下为解决的记录。



不能上网的电脑是ubuntu 18.04，通过systemd来启动docker，可以通过重载默认的`docker.service`文件来配置代理：

1. 首先创建一个目录

```shell
$ sudo mkdir /etc/systemd/system/docker.service.d
```

2. 然后在这个目录放置代理配置文件，起名为`socks5-proxy.conf`

```shell
$ cd /etc/systemd/system/docker.service.d
$ sudo vim socks5-proxy.conf
```

3. 文件内容为代理信息

```
[Service]
Environment="ALL_PROXY=socks5://代理服务器IP地址:端口"
```

4. 重载配置，并查看是否有相应配置，Environment=相应配置即为配置成功

```
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
$ sudo systemctl show --property Environment docker
Environment=ALL_PROXY=socks5://代理服务器IP地址:端口
```

5. 验证下工作是否正常

```
$ sudo docker pull ubuntu:xenial
xenial: Pulling from library/ubuntu
7e6591854262: Pull complete
089d60cb4e0a: Pull complete
9c461696bc09: Pull complete
45085432511a: Pull complete
Digest: sha256:599b12ff9760b68095db78eaf1260e53c8839ca5ff590fb4a3d2f79c8d459b2b
Status: Downloaded newer image for ubuntu:xenial
```



