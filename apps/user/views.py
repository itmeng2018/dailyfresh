import re

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

# Create your views here.

# /user/register
from apps.user.models import User


def register(request):
    '''
    显示注册页面
    :param request:
    :return:
    '''
    return render(request, 'register.html')


def register_handle(request):
    '''
    进行注册处理
    :param request:
    :return: Z
    '''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    confirm_pwd = request.POST.get('cpwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    # 进行数据完整性校验
    if not all((username, password, email)):
        # 数据不完整
        return render(request, 'register.html', {'errmsg': '数据不完整'})

    # 判断用户名是否重复
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 查询异常说明用户名不存在
        user = None

    if user:    # 用户名已存在
        return render(request, 'register.html', {'errmsg': '用户名已存在'})


    # 校验两次密码
    if password != confirm_pwd:
        return render(request, 'register.html', {'errmsg': '两次密码不一致'})

    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

    # 校验是否同意协议
    if allow != 'on':
        render(request, 'register.html', {'errmsg': '未勾选”天天生鲜用户使用协议“'})

    # 进行业务逻辑处理: 进行用户注册
    user = User.objects.create_user(username, email, password)
    user.is_active = 0
    user.save()

    # 返回应答, 跳转到首页
    print(reverse('goods:index'))
    return redirect(reverse('goods:index'))
