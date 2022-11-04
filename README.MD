## 这是一个快速将图片/小文件上传到腾讯云COS的脚本
> But...
#### 为什么要把腾讯云COS用作图床呢？
- [x] 自建图床/文件有着较高的稳定性，再也不用担心Markdown中引用的图片无法显示
- [x] 用作图床/文件床时，腾讯云COS较实惠，一年仅需10元左右就可拥有60G COS(2022.11)
#### 为什么要用脚本而不是原生网页上传文件？
- [x] 可以大幅度简化上传流程（哈哈哈哈网页端上传真的太费事了）

<img src="https://pkpublicdoc-1314730533.cos.ap-beijing.myqcloud.com/PICUP.png" width="20%">

### 功能介绍
本脚本目前可以：
- [x] 一次上传单个文件/文件夹
- [x] 上传文件时可选随机文件名，省心省事
- [x] 上传时检测文件名是否重复，避免覆盖COS内原文件
- [x] 上传较大文件时显示上传进度条，便于跟踪上传状态
- [x] 本地加密保存API密钥等个人参数（[参考 the-javapocalypse/Python-File-Encryptor](https://github.com/the-javapocalypse/Python-File-Encryptor)）
----
### 使用方法
直接转到Releases，下载.exe文件即可

### 部署方法
1. 购买腾讯云COS资源，并**至少创建两个**[存储桶](https://console.cloud.tencent.com/cos/bucket)  
注意：存储桶权限须设置为**公有读私有写**
2. 为脚本[申请API密钥](https://console.cloud.tencent.com/cam/capi)
3. 安装需要的python包
 ```
pip install -U cos-python-sdk-v5
pip install tkinter
pip install faker
pip install tqdm
```
4. 打开`main.py`
5. 可以愉快的食用了 :)

### 开发环境
- PyCharm 2022.2.2 
- VS Code 1.73.0
- Python 3.11（编写/测试）
- Python 3.9（exe打包）

### 已知Bug
- 文件最多选择1000个

### 待填坑
- [x] 错误处理
- [x] 增强安全性（双校验）
- [x] 增强安全性（尽量变量保存key）
- [ ] 进度条改进

### Licence
**MIT Licence**

### 写在最后
- 由于作者是python小白，代码难免会有bug，欢迎各位发issue   
~~PS.真的有人会看到我这个破脚本吗hhhh~~
- ~~这个就是作者自己折腾玩的东西，要是出错不必在意~~，推荐大家使用诸如[PicGo](https://github.com/Molunerfinn/PicGo)等稳定成熟的图床软件 :)