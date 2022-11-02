import logging
import os
import sys
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import tkinter as tk
from tkinter import filedialog
from faker import Faker
f = Faker(locale='zh_CN')
root = tk.Tk()
root.withdraw()
timex = 0
isreturn = 1
isallfak = 0
address = [0]*100000
cos_secret = [0] * 5
secret_id='none'
secret_key='none'
region='none'
def writeio():
    global cos_secret
    global secret_id
    global secret_key
    global region
    filecos_ok = 0
    while (filecos_ok != 1):
        if os.path.exists('COS.secret'):
            filepath = 'COS.secret'
            with open(filepath, 'r', encoding='UTF-8') as file:
                timel = 0
                for line in file:
                    cos_secret[timel] = line.strip()
                    timel = timel + 1
            filecos_ok = 1
            print("==COS参数加载完成==\n")
        else:
            f = open("COS.secret", "x")
            print("当前不存在COS参数，请输入参数\n")
            f.write(input("输入secretid\n") + "\n")
            f.write(input("输入secretkey\n") + "\n")
            f.write(input("输入Region\n") + "\n")
            f.write(input("输入图片库名\n") + "\n")
            f.write(input("输入文档库名\n") + "\n")
            f.close()
    secret_id=cos_secret[0]
    secret_key=cos_secret[1]
    region=cos_secret[2]

def uploada(bucketx):
    print("请选择你要上传的文件")
    filepathall = filedialog.askopenfilename()  # 获得选择好的文件
    uploadfile(filepathall)

def uploadb(bucketx):
    global isallfak
    Folderpath = filedialog.askdirectory()
    bucket = bucketx
    isallfak1 = input("是否全部使用随机文件名？\nY)使用\nN)不使用\n")
    if (isallfak1 == 'Y'):
        isallfak = 1
    if (isallfak1 == 'N'):
        isallfak = 0
    g = os.walk(Folderpath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepathall = Folderpath+"/"+file_name
            uploadfile(filepathall)

def uploadfile(filepathall):
    ##### -----1.连接桶部分-----#####
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("=====连接存储桶...=====")
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
    print("本地上传文件地址为"+filepathall)
##### -----4.判断桶种有无重名项-----#####
    response = client.object_exists(
        Bucket=bucketx,
        Key=filename)
    while response == True:
        print("将要上传的文件与库中已有项重名")
        print("是否重命名文件？")
        tod = input("A->重命名\nB->随机文件名\nC->继续上传\n")
        if (tod == 'A'):
            filename = input("请重新输入文件名\n")+fileext
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
    response = client.upload_file(
        Bucket=bucketx,
        Key=filename,
        LocalFilePath=filepathall,
        EnableMD5=False,
        progress_callback=None
    )
##### -----6.总结-----#####
    global timex
    global address
    print("╔══════════════════╗")
    print("║     上传成功！   ║")
    print("╚══════════════════╝")
    if lib == 1:
        address[timex] = 'https://'+cos_secret[3]+'.cos.ap-beijing.myqcloud.com/'+filename
        print("===>>本次上传文件地址为", address[timex])
        timex = timex+1
    if lib == 2:
        address[timex] = 'https://'+cos_secret[4]+'.cos.ap-beijing.myqcloud.com/'+filename
        print("===>>本次上传文件地址为", address[timex])
        timex = timex+1

##### ==========入口==========#####
while (isreturn == 1):
    print("╔══════════════════════════════╗")
    print("║    COS图床文件上传脚本       ║")
    print("║    v1.6 By pk5 2022-10-31    ║")
    print("╚══════════════════════════════╝")
    writeio()
    lib = int(input("请选择要上传的库\n1->图片库\n2->文档库\n"))
    if lib == 1:
        bucketx = cos_secret[3]
    if lib == 2:
        bucketx = cos_secret[4]
    if (lib < 1 or lib > 2):
        input("您输入类型有误，请重开！\n")
        sys.exit()
    dow = input("A->单个上传\nB->批量上传\n")
    if (dow == 'A'):
        uploada(bucketx)
    if (dow == 'B'):
        uploadb(bucketx)
    print("╔═════════════════════════════════════════════╗")
    print("║      全部上传完毕！现在输出上传文件地址     ║")
    print("╚═════════════════════════════════════════════╝")
    for n in range(0, timex):
        print(address[n])
    nextx = input("按N继续上传\n")
    if (nextx == 'N'):
        for i in range(0,100000):
            address[i]=0
        isreturn = 1
    else:
        isreturn = 0
