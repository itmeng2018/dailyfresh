# 天天生鲜

### 一. 项目架构

![项目架构](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/项目架构.png)

### 二. 模块设计

- 用户模块
- 商品模块
- 购物车模块
- 订单模块
- 后台模块

### 三. 数据库设计

![数据库设计-大](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/数据库设计-大.png)

![数据库设计](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/数据库设计.png)

### 四. 页面设计

![页面设计](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/页面设计.png)

### 五. 功能设计

![功能设计](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/功能设计.png)

### 六. 开发环境

1. 操作系统: MacOS 10.14.1

2. python3.5.6

3. 模块版本

   > django==1.8.19
   >
   > pymysql==0.9.2
   >
   > redis==2.10.6
   >
   > django-redis==4.10.0
   >
   > django-redis-sessions==0.5.6
   >
   > django-tinymce==2.6.0
   >
   > itsdangerous==1.1.0
   >
   > pillow==5.3.0
   >
   > celery==4.2.1

 ### 七. 服务器环境

    1. 操作系统 Ubuntu16.04 LTS
    2. 服务端 Nginx + uwsgi + python3.5.6
    3. mysql + redis + FastDFS + django

### 八. 开发计划

    1. 用户注册
    2. 用户登录
    3. 用户中心
    4. 分布式FastDFS文件系统
    5. 首页
    6. 详情页
    7. 列表页
    8. 搜索功能和搜索页
    9. 购物车
    10. 订单生产
    11. 订单并发处理
    12. 订单支付
    13. 订单评论
    14. 服务器部署

### 九. 技术总结

    1. django默认的认证系统 AbstractUser
    2. itsdangerous 生成签名的token, 序列化工具:dumps/loads
    3. 邮件 django, send_mail, celery+redis实现异步任务
    4. 搜索 haystack+whoosh索引/分词
    5. 页面静态化 celery+nginx, 负载平衡, 缓解服务器压力
    6. 缓存(保存的位置, 有效期, 与数据库的一致性问题)
    7. 购物车redis-hash   历史记录redis-list
    8. 前段用ajax请求后端接口
    9. 高并发的库存问题(悲观锁, 乐观锁)
    10. 订单支付, 支付宝接口
