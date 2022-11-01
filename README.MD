## 这是一个快速将图片/小文件上传到腾讯云COS的脚本
> 不过...
#### 为什么要把腾讯云COS用作图床呢？
- [x] 自建图床/文件有着较高的稳定性，再也不用担心Markdown中引用的图片无法显示
- [x] 用作图床/文件床时，腾讯云COS较实惠，一年仅需10元左右就可拥有60G COS(2022.11)
#### 为什么要用脚本而不是原生网页上传文件？
- [x] 可以大幅度简化上传流程（哈哈哈哈网页端上传真的太费事了）
### 功能介绍
本脚本目前可以：
- [x] 一次上传一个/多个文件
- [x] 上传时检测文件名是否重复，避免覆盖COS内原文件
- [x] 上传文件时随机文件名，省心省事
----
### 使用方法
1. 购买腾讯云COS资源，并**至少创建两个**[存储桶](https://console.cloud.tencent.com/cos/bucket)  
注意：存储桶权限须设置为**公有读私有写**
1. 为脚本[申请API密钥](https://console.cloud.tencent.com/cam/capi)
2. 安装需要的python包
 ```
pip install -U cos-python-sdk-v5
pip install tkinter
pip install faker
```
4. 打开`main.py`后，输入API密钥、所属地域和两个存储桶名称
![API密钥](https://pub-bj-pic-1314730533.cos.ap-beijing.myqcloud.com/ptlQAJZUUKCmxmzRRRKA.png)
![地域](https://pub-bj-pic-1314730533.cos.ap-beijing.myqcloud.com/JGnkeksyXhrbZJeuypxZ.png)
5. 可以愉快的食用了:)
### 已知Bug
- 文件最多选择1000个

### 待填坑
-[ ] 错误处理

由于作者是python小白，代码难免会有bug，欢迎各位发issue   
~~PS.真的有人会看到我这个破脚本吗hhhh~~