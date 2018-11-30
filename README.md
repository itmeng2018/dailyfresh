# 天天生鲜

### 一. 项目架构

![项目架构](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/01-%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1.png)

### 二. 页面设计

![页面设计](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/02-%E9%A1%B5%E9%9D%A2%E8%AE%BE%E8%AE%A1.png)

### 三. 功能设计
![功能设计](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/03-%E5%8A%9F%E8%83%BD%E8%AE%BE%E8%AE%A1.png)

### 四. 数据库设计

![数据库设计-大](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/04-%E6%95%B0%E6%8D%AE%E5%BA%93%E8%AE%BE%E8%AE%A1-%E5%A4%A7.png)

![数据库设计](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/04-%E6%95%B0%E6%8D%AE%E5%BA%93%E8%AE%BE%E8%AE%A1.png)

### 五. celery

![celery](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/05-celery.png)

### 六. FastDFS

![FastDFS](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/06-fastDFS.png)

### 七. 服务器部署

![服务器](https://github.com/itmeng2018/dailyfresh/blob/master/rede_image/07-%E6%9C%8D%E5%8A%A1%E5%99%A8.png)


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
    8. 前段用ajax-post请求后端接口
    9. 高并发的库存问题(悲观锁, 乐观锁)
    10. 订单支付, 支付宝接口

