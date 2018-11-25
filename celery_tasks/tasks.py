import time

# 使用celery
from celery import Celery

from django.conf import settings
from django.core.mail import send_mail

# ------------------------
# worker code:
# import os
# import django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()
# ------------------------
# TODO 异步邮件发送配置
# 创建一个Celery的实例对象 -- broker: 任务队列(中间人)
# app = Celery('celery_tasks.tasks', broker='redis://139.196.137.234:6379/8')  # aliyun
app = Celery('celery_tasks.tasks', broker='redis://192.168.154.129:6379/8')  # work_ubuntu


# 定义发邮件任务函数
@app.task
def send_register_active_email(to_email, username, token):
    '''
    发送激活邮件
    :param to_email: 收件人
    :param username: 用户名
    :param token: 用户id生成的token
    '''
    # 组织邮件信息
    subject = '感谢您注册天天生鲜'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br /><a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/%s/</a>' % (
        username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
