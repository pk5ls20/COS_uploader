### writeio函数：
#### - 不存在COS.secret.enc（此时也一定不存在密码）
1. 进入compass
2. 创建COS.secret
3. 用户录入COS.secret
4. 进入writeio2
#### - 存在COS.secret.enc(此时一定存在密码)
1. 要求compass
2. 调用函数：删除COS.secret.enc，得到COS.secret
3. 进入writeio2
### writeio2函数
1. **将COS.secret内容进入列表变量中**
2. **调用函数：删除COS.secret，得到COS.secret.enc**
### compass函数
- 判断是否存在密码
> 如果不存在：
> 1. 要求用户输入密码
> 2. 将输入密码创建为SPA.secret
> 3. 对SPA.secret加密
> 4. 返回true

> 如果存在：
> 1. 要求用户输入密码
> 2. 将SPA.secret.enc解密
> 3. 对比值
> 3. 若一样，返回true，否则false