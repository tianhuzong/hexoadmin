# hexoadmin
An admin for hexo.一个为hexo编写的后台

## 作者简介
- 作者：仙
- email：tianhuzong@qq.com
- github: [tianhuzong](https://github.com/tianhuzong)
- gitee: [gitee](https://gitee.com/thzsen)
- bilibili: [天狐宗仙](https://space.bilibili.com/3494354284972407)
- 爱发电: [thzsen](https://afdian.net/a/thzsen)

## 项目简介
本项目采用flask开发，支持`python3.8+`,由于使用hexo创建文章必须进入终端，比较麻烦，为了解决这个麻烦，特此开发`hexoadmin`。
本项目提供了API可供其他语言接入，之后可能还会提供一个前端进行操作，由于本人精力有限，可能功能不是很齐全，有bug请在[github issue](https://github.com/tianhuzong/hexoadmin/issues)
- github地址： [tianhuzong/hexoadmin](https://github.com/tianhuzong/hexoadmin)
- gitee地址：[thzsen/hexoadmin](https://gitee.com/thzsen/hexoadmin)


```
为了保证数据不被篡改，向服务器发送请求时必须带有签名，服务器返回内容也会带有签名，客户端收到数据后需要验证签名已保证数据完整性
```

## 签名验证
### 基本实现方法
将发送到服务器的内容和服务器返回的内容data节点下的内容按照key从小到大进行排序用`&`进行拼接转换成网址的形式，例如：
请求体为:
```json
{
    "data":{
        "path":"/usr/bin",
        "content":"test"
    }
}
```
转换成网址:
```
content=test&path=/usr/bin
```
然后拼接上APIkey
```
content=test&path=/usr/bin&APIkey=YOUR_APIKEY
```
取MD5
```
fcce4a6c91c9aa95bef3d979a860aaaf
```
那最后请求体就是
```json
{
    "data":{
        "path":"/usr/bin",
        "content":"test"
    },
    "sign":"fcce4a6c91c9aa95bef3d979a860aaaf"
}
```

如果在get请求中https://domain/api?a=b&c=d
那就直接
```
md5("a=b&c=d&APIkey=YOUR_APIKEY")
```
把结果拼接在URL后面就好，即`https://domain/api?a=b&c=d&sign=759adc69c70497aa326dc109b4cf0d33`
遇到path参数的话
<kbd>https://domain/api/{pk}/{xxx}</kbd>
那就变成`pk=1&xxx=xxx`的形式，拼接上APIkey，取md5就可以了。

### 签名代码

#### utils
```python
import json
import hashlib
def json2pathValue(json_object):
    json_dict = json.loads(json_object)
    key_list = sorted(list(json_dict.keys()))
    result = []
    for key in key_list:
        value = json_dict[key]
        if value is None or value == "":
            result.append(f"{key}=")
        else:
            result.append(f"{key}={value}")
    return "&".join(result).replace("'",'"').replace(" ","")

def md5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()

"""下面是sign签名的函数"""
def sign(jsondata:str,APIkey):
    """
    sign签名函数
    :param jsondata json字符串
    :param APIkey 你的apikey
    :return 返回sign签名
    """
    return md5(json2pathValue(jsondata)+f"&APIkey={APIkey}")
```

```
get请求除了直接把a=b&c=d直接排序以外也可以转成json数据然后调用上面的`sign`函数，如果一个api具有url参数和path参数，那么url参数和path参数要同时放到一起排序
```