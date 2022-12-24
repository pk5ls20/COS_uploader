# 引入库
import os
import sys
import linecache
import atexit
import logging
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
addressl = [0] * 100000
cos_secret = [0] * 10
secret_id = 'none'
secret_key = 'none'
region = 'none'
timex3 = 0
pas0 = ''
a_key = [0] * 10
a_pas = ''
global pb

# 最后不要忘了删除明文
def del_db_run_away():
    if os.path.exists('SPA.secret'):
        enc.encrypt_file('SPA.secret')
    if os.path.exists('COS.secret'):
        enc.encrypt_file('COS.secret')


# 函数：比较密码：
def comparex():
    pasin_ = input("请输入密码：\n")
    if pasin_ == a_pas:
        return True
    else:
        return False


def writeio():
    global a_key
    global a_pas
    try:
        if a_key[0] != 0 and a_pas != '':
            if comparex():
                return True
            else:
                return False
        else:
            if os.path.exists('COS.secret.enc') and os.path.exists('SPA.secret.enc'):
                # decrypt COS.secret.enc First
                enc.decrypt_file('COS.secret.enc')
                # writein COS.secret in a_key
                with open('COS.secret', 'r', encoding='UTF-8') as file:
                    time_cos = 0
                    for line in file:
                        a_key[time_cos] = line.strip()
                        time_cos = time_cos + 1
                enc.encrypt_file('COS.secret')
                # And then decrypt SPA.secret
                enc.decrypt_file('SPA.secret.enc')
                file = open('SPA.secret', 'r')
                a_pas = file.readline()
                file.close()
                enc.encrypt_file('SPA.secret')
                # start to compare password
                if a_key[5] == a_pas:
                    if comparex():
                        return True
                    else:
                        return False
                else:
                    print("参数错误，请删除同目录文件后重新打开文件！")
                    return False
            else:
                pas0 = input("请输入初始密码！\n")
                a_pas = pas0
                ff = open("SPA.secret", "w")
                ff.write(pas0)
                ff.close()
                enc.encrypt_file('SPA.secret')
                fx = open("COS.secret", "w")
                print("当前不存在COS参数，请输入参数\n")
                # 3.录入COS.secret
                fx.write(input("输入secretid\n") + "\n")
                fx.write(input("输入secretkey\n") + "\n")
                fx.write(input("输入Region\n") + "\n")
                fx.write(input("输入图片库名\n") + "\n")
                fx.write(input("输入文档库名\n") + "\n")
                fx.write(a_pas)
                fx.close()
                enc.encrypt_file('COS.secret')
                return True
    except IOError:
        exitx2()


# 函数：单个选择文件询问
def uploada(bucketx):
    print("请选择你要上传的文件\n")
    filepathall = filedialog.askopenfilename()  # 获得选择好的文件
    if filepathall == '': exitx()
    uploadfile(filepathall)


# 函数：多个选择文件询问
def uploadb(bucketx):
    global isallfak
    Folderpath = filedialog.askdirectory()
    bucket = bucketx
    if Folderpath == '': exitx()
    isallfak1 = input("是否全部使用随机文件名？\nY)使用\nN)不使用\n")
    if (isallfak1 == 'Y'):
        isallfak = 1
    else:
        if (isallfak1 == 'N'):
            isallfak = 0
        else:
            exitx()
    g = os.walk(Folderpath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepathall = Folderpath + "/" + file_name
            uploadfile(filepathall)


class pbar_x:
    def __init__(self,size):
        self.pbar = tqdm(total=size*1.03, colour='green')

    def update(self, num):
        self.pbar.update(num)

    def close(self):
        self.pbar.close()


# 函数：进度条回调，计算当前上传的百分比
def upload_percentage(consumed_bytes, total_bytes):
    # 进度条回调函数，计算当前上传的百分比
    ratex = 0
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        pb.update(rate - ratex)
        ratex = rate


# 函数：上传文件主函数
def uploadfile(filepathall):
    global timex
    global address
    global addressl
    global pb
    try:
        ##### -----1.连接桶部分-----#####
        # logging.basicConfig(level=logging.INFO, stream=sys.stdout)  # 输出日志，可以去掉qwq
        print("开始上传...")
        config = CosConfig(Region=a_key[2], SecretId=a_key[0],
                           SecretKey=a_key[1], Token=None, Scheme='https')  # type: ignore
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
        addressl[timex] = filepathall
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
        f_size = os.path.getsize(filepathall)
        if f_size > 20971520:
            pb = pbar_x(f_size / 1024 / 1024 * 50)
        response = client.upload_file(
            Bucket=bucketx,
            Key=filename,
            LocalFilePath=filepathall,
            EnableMD5=False,
            progress_callback=upload_percentage
        )
        ##### -----6.总结-----#####
        if f_size > 20971520:
            pb.close()
        print("上传成功！")
        if lib == 1:
            address[timex] = 'https://' + str(a_key[3]) + '.cos.' + str(a_key[2]) + '.myqcloud.com/' + filename
            timex = timex + 1
        if lib == 2:
            address[timex] = 'https://' + str(a_key[4]) + '.cos.' + str(a_key[2]) + '.myqcloud.com/' + filename
            timex = timex + 1
    except (CosServiceError, CosClientError):
        input("上传COS中出现异常\n请确定参数是否正确以及网络是否畅通\n程序即将退出！")
        sys.exit()


def exitx():
    input("您输入类型/选择类型有误，请重开！\n")
    sys.exit()


def exitx2():
    print("读取参数失败，程序即将退出！")
    sys.exit()


##### ==========入口==========#####
atexit.register(del_db_run_away)
while (isreturn == 1):
    print("╔══════════════════════════════╗")
    print("║     COS图床文件上传脚本      ║")
    print("║   v1.10  By pk5 2022-12-25   ║")
    print("╚══════════════════════════════╝")
    while writeio() == False:
        print("密码错误，请重新输入！\n")
    try:
        lib = int(input("请选择要上传的库\n1->图片库\n2->文档库\n"))
        if lib == 1:
            bucketx = a_key[3]
        else:
            if lib == 2:
                bucketx = a_key[4]
            else:
                exitx()
    except ValueError:
        exitx()
    dow = input("A->单个上传\nB->批量上传\n")
    if dow == 'A':
        uploada(bucketx)
    if dow == 'B':
        uploadb(bucketx)
    if dow != 'A' and dow != 'B':
        exitx()
    print("╔═════════════════════════════════════════════╗")
    print("║      全部上传完毕！现在输出上传文件地址     ║")
    print("╚═════════════════════════════════════════════╝")
    for n in range(0, timex):
        print("本地地址：", end=str(addressl[n]))
        print("\n")
        print("文件链接：", end=str(address[n]))
        print("\n")
    nextx = input("按N继续上传\n")
    if (nextx == 'N'):
        for i in range(0, 100000):
            address[i] = 0
        isreturn = 1
    else:
        isreturn = 0
