from tqdm import tqdm
import time

pbar = tqdm(total=200) # 设置总长度
for i in range(100):
    time.sleep(0.05)
    # 每次更新进度条的长度
    pbar.update(1) # 相当于在当前长度的基础上 +1 的操作

pbar.close()
