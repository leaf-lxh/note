#### 大吉大利,今晚吃鸡~

> <http://117.51.147.155:5050/index.html#/login>

注册登进去看看

在app.js里找到了很多路径

```
                path: "/main/index",
                component: D.default
            }), u.default.createElement(N.Route, {
                path: "/main/pay",
                component: a.default
            }), u.default.createElement(N.Route, {
                path: "/main/result",
                component: r.default
            }), u.default.createElement(N.Redirect, {
                to: "/main/index"
```

其中访问/main/result可以直接看到获得入场券和礼包的提示，但是因为没有买票所以没什么用



余额只有100，但是买票时票价是2000，支付时会提示余额不足

用burpsuite抓包修改，发现最多只能改到1000，再低甚至到负数都不行。

试了下注入没成功



谷歌了一下支付时服务器返回的pay-server报文头(Apache-Coyote)，发现后端是Java写的。打算尝试用整数溢出来绕过不能低于1000的限制。

一开始假设是long类型，传递过去Long.MAX_VALUE(2的63次方)9223372036854775807，发现前端显示的票价数据被四舍五入了（9223372036854776000）。再增大数值服务器会报500错误

试了一下Integer.MAX_VALUE+1，为int最小值，虽然能买到票，但是无法支付，支付服务器报500错误，

尝试溢出成0，传递过去-1的无符号值+1（4294967295 + 1）， 能成功支付。

又注册了一个小号，票价改为4294967295 + 1 + 100，也能支付成功，而且余额变成了0。可能后端对负数的数值进行了检测



然后提供了一个ID和ticket，点击移除对手，要求提供ID和ticket

提交自己的发现信息发现不行，注册了一个小号提交过去，提交成功但是发现剩余对手没变。自己的ID是116，可能要提交100个以上的对手。篡改了一下小号的ticket值，提交过去发现会提示参数错误。看ticket的值像是一个MD5,而且加了盐。想了一下想试试长度扩展攻击来绕过MD5合法性的校验，不过只做过PHP后端实现的题，不确定java后端能否攻击成功。



于是老老实实写脚本注册了将近一千个账号........发现ID最小1，最大149，每个ID对应唯一的一个ticket值

提交过去，拿到了flag



写这篇wp的时候想了一下如果盐很短的话或许可以把盐暴力枚举出来