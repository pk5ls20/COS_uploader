# 引入库
import os
import sys
import linecache
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
import tkinter as tk
from tkinter import filedialog
from faker import Faker
from tqdm import tqdm
from Encryptor import enc

# 初始变量设定
f = Faker(locale='zh_CN')
root = tk.Tk()
root.withdraw()
timex = 0
isreturn = 1
isallfak = 0
filecos_ok = 0
address = [0] * 100000
addressl= [0] * 100000
cos_secret = [0] * 10
secret_id = 'none'
secret_key = 'none'
region = 'none'
timex3=0
pas0=''

# 函数：比较密码：
def compass():
    global pas0
    try:
        global timex3
        if os.path.exists('SPA.secret.enc'):
            l = str(input("请输入参数密码\n"))
            enc.decrypt_file('SPA.secret.enc')
            file = open('SPA.secret', 'r')
            if file.readline() == l:
                # 双校验
                enc.decrypt_file('COS.secret.enc')
                if linecache.getline('COS.secret', 6) == l+'\n':
                    file.close()
                    enc.encrypt_file('COS.secret')
                    enc.encrypt_file('SPA.secret')
                    return True
                else:
                    file.close()
                    print("密码校验失败！")
                    enc.encrypt_file('COS.secret')
                    enc.encrypt_file('SPA.secret')
                    return False
            else:
                file.close()
                enc.encrypt_file('SPA.secret')
                return False
        else:
            if os.path.exists('COS.secret.enc'):
                print("当前存在无效参数，请删除同目录下COS.secret.enc后重试！\n")
                if timex3==1: sys.exit()
                timex3=1
                return False
            else:
                pas0=input("请输入初始密码！\n")
                ff = open("SPA.secret", "w")
                ff.write(pas0)
                ff.close()
                enc.encrypt_file('SPA.secret')
                return True
    except IOError: exitx2()

# 函数：读取参数
def writeio2():
    try:
        # 目前存在COS.secret
        # 需要将COS.secret录入list，然后将COS.secret重新加密
        global cos_secret
        global secret_id
        global secret_key
        global region
        global filecos_ok
        # 1.将COS.secret内容进入列表变量中
        with open('COS.secret', 'r', encoding='UTF-8') as file:
            timel = 0
            for line in file:
                cos_secret[timel] = line.strip()
                timel = timel + 1
        secret_id = cos_secret[0]
        secret_key = cos_secret[1]
        region = cos_secret[2]
        print("===COS参数加载完成===\n")
        # 2.调用函数：删除COS.secret，得到COS.secret.enc
        enc.encrypt_file('COS.secret')
        filecos_ok = 1
    except IOError: exitx2()

# 函数：写入参数
def writeio():
    global pas0
    try:
        writer = 0
        while filecos_ok != 1:
            # 注意，这个判定要改的
            if os.path.exists('COS.secret.enc'):
                # 存在 COS.secret.enc
                # 1.进入密码函数
                if compass():
                    # 2.调用函数：删除COS.secret.enc，得到COS.secret
                    enc.decrypt_file('COS.secret.enc')
                    # 3.进入writeio2
                    writeio2()
                else:
                    print("密码输入错误，请重新输入！\n")
            else:
                # 不存在COS.secret.enc
                # 1.进入密码函数
                compass()
                # 2.创建COS.secret
                fx = open("COS.secret", "w")
                print("当前不存在COS参数，请输入参数\n")
                # 3.录入COS.secret
                fx.write(input("输入secretid\n") + "\n")
                fx.write(input("输入secretkey\n") + "\n")
                fx.write(input("输入Region\n") + "\n")
                fx.write(input("输入图片库名\n") + "\n")
                fx.write(input("输入文档库名\n") + "\n")
                fx.write(pas0)
                fx.close()
                # 4.进入writeio2
                writeio2()
    except IOError: exitx2()

# 函数：单个选择文件询问
def uploada(bucketx):
    print("请选择你要上传的文件\n")
    filepathall = filedialog.askopenfilename()  # 获得选择好的文件
    if filepathall=='':exitx()
    uploadfile(filepathall)

# 函数：多个选择文件询问
def uploadb(bucketx):
    global isallfak
    Folderpath = filedialog.askdirectory()
    bucket = bucketx
    if Folderpath=='': exitx()
    isallfak1 = input("是否全部使用随机文件名？\nY)使用\nN)不使用\n")
    if (isallfak1 == 'Y'): isallfak = 1
    else:
        if (isallfak1 == 'N'): isallfak = 0
        else: exitx()
    g = os.walk(Folderpath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepathall = Folderpath + "/" + file_name
            uploadfile(filepathall)

# 函数：进度条回调，计算当前上传的百分比
def upload_percentage(consumed_bytes, total_bytes):
    # 进度条回调函数，计算当前上传的百分比
    ratex=0
    pbar = tqdm(total=100)
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        pbar.update(rate-ratex)
        ratex=rate
    pbar.close()

# 函数：上传文件主函数
def uploadfile(filepathall):
    global timex
    global address
    global addressl
    try:
        ##### -----1.连接桶部分-----#####
        # logging.basicConfig(level=logging.INFO, stream=sys.stdout) # 输出日志，可以去掉qwq
        print("开始上传...")
        token = None
        scheme = 'https'
        config = CosConfig(Region=region, SecretId=secret_id,
                        SecretKey=secret_key, Token=token, Scheme=scheme)  # type: ignore
        client = CosS3Client(config)
        ##### -----2.引入分割文件名os-----#####
        (ext, filename) = os.path.splitext(filepathall)
        fileext = filename
        (path, filename) = os.path.split(filepathall)
        filepath0 = path
        ##### -----3.询问随机文件名-----#####
        if (isallfak == 0):
            isfaker = input("是否使用随机文件名？（建议图床使用）\nY)使用\nN)不使用\n")
            if (isfaker == 'Y'):
                filename = f.pystr() + fileext
        if (isallfak == 1):
            filename = f.pystr() + fileext
        addressl[timex]=filepathall
        ##### -----4.判断桶种有无重名项-----#####
        response = client.object_exists(
            Bucket=bucketx,
            Key=filename)
        while response == True:
            print("将要上传的文件与库中已有项重名")
            print("是否重命名文件？")
            tod = input("A->重命名\nB->随机文件名\nC->继续上传\n")
            if (tod == 'A'):
                filename = input("请重新输入文件名\n") + fileext
            if (tod == 'B'):
                filename = f.pystr() + fileext
            if (tod == 'C'):
                tod2 = input("警告：继续将覆盖原文件，是否继续？\n->Y/N\n")
                if (tod2 == 'Y'):
                    break
                if (tod2 == 'N'):
                    continue
                else:
                    print("输入有误，重开吧...")
                    continue
            if (tod != 'A' and tod != 'B' and tod != 'C'):
                print("输入有误，重开吧...\n")
                continue
            response = client.object_exists(
                Bucket=bucketx,
                Key=filename)
        ##### -----5.开始上传-----#####
        print("开始上传啦~")
        response = client.upload_file(
            Bucket=bucketx,
            Key=filename,
            LocalFilePath=filepathall,
            EnableMD5=False,
            progress_callback=upload_percentage
        )
        ##### -----6.总结-----#####
        print("上传成功！")
        if lib == 1:
            address[timex] = 'https://' + cos_secret[3] + '.cos.' + cos_secret[2] + '.myqcloud.com/' + filename
            timex = timex + 1
        if lib == 2:
            address[timex] = 'https://' + cos_secret[4] + '.cos.' + cos_secret[2] + '.myqcloud.com/' + filename
            timex = timex + 1
    except (CosServiceError,CosClientError):
        input("上传COS中出现异常\n请确定参数是否正确以及网络是否畅通\n程序即将退出！")
        sys.exit

def exitx():
    input("您输入类型/选择类型有误，请重开！\n")
    sys.exit()

def exitx2():
    print("读取参数失败，程序即将退出！")
    sys.exit()

##### ==========入口==========#####
while (isreturn == 1):
    print("╔══════════════════════════════╗")
    print("║     COS图床文件上传脚本      ║")
    print("║   v1.9.0 By pk5 2022-11-04   ║")
    print("╚══════════════════════════════╝")
    writeio()
    try:
        lib = int(input("请选择要上传的库\n1->图片库\n2->文档库\n"))
        if lib == 1: bucketx = cos_secret[3]
        else:
            if lib == 2: bucketx = cos_secret[4]
            else: exitx()
    except ValueError: exitx()
    dow = input("A->单个上传\nB->批量上传\n")
    if dow == 'A':
        uploada(bucketx)
    if dow == 'B':
        uploadb(bucketx)
    if dow!='A'and dow!='B':
        exitx()
    print("╔═════════════════════════════════════════════╗")
    print("║      全部上传完毕！现在输出上传文件地址     ║")
    print("╚═════════════════════════════════════════════╝")
    for n in range(0, timex):
        print("本地地址：",end=addressl[n])
        print("\n")
        print("文件链接：",end=address[n])
        print("\n")
    nextx = input("按N继续上传\n")
    if (nextx == 'N'):
        for i in range(0, 100000):
            address[i] = 0
        isreturn = 1
    else:
        isreturn = 0