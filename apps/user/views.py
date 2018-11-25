import re

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django_redis import get_redis_connection

from user.models import User, Address
from goods.models import GoodsSKU
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin


# /user/register
class RegisterView(View):
    '''注册'''

    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/(user_id_token)

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()

        # 发邮件
        send_register_active_email.delay(email, username, token)

        # 返回应答, 跳转到首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''用户激活'''

    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')


# /user/login
class LoginView(View):
    '''登录'''

    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)

                # 获取用户登录后要跳转到的地址
                next_url = request.GET.get('next', reverse('goods:index'))

                # 跳转到next_url(默认首页)
                response = redirect(next_url)

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# /user/logout
class LogoutView(View):
    '''退出登录'''

    def get(self, request):
        '''
        退出登录
        :param request:
        :return: 首页
        '''
        # 登出用户 - 清除用户的session信息
        logout(request)
        # 跳转到首页
        return redirect(reverse('goods:index'))


# /user/
class UserInfoView(LoginRequiredMixin, View):
    '''用户中心-信息页'''

    def get(self, request):
        '''
        显示
        :param request:
        :return: 用户信息页
        '''
        # 用户个人信息展示
        user = request.user
        address = Address.objects.get_default_address(user)

        # 用户历史浏览记录展示  -- 使用redis存储(user_id:list)
        # 使用setting中的redis.default配置创建StrictRedis()的实例对象
        con = get_redis_connection("default")

        # 获取用户的历史浏览记录
        history_key = 'history_%d' % user.id

        # 获取用户最近浏览的5条商品id
        sku_ids = con.lrange(history_key, 0, 4)

        # 遍历获取ids, 单个进行数据库查询,避免数据库查询的id自动升序问题与浏览顺序冲突问题
        goods_list = [GoodsSKU.objects.get(id=i) for i in sku_ids]

        # 组织上下文
        context = {
            'page': 'user',
            'address': address,
            'goods_list': goods_list,
        }

        return render(request, 'user_center_info.html', context)


# /user/order/
class UserOrderView(LoginRequiredMixin, View):
    '''用户中心-订单页'''

    def get(self, request):
        '''
        显示
        :param request:
        :return: 用户订单页
        '''
        # 获取用户的订单信息

        return render(request, 'user_center_order.html', {'page': 'order'})


# /user/address/
class AddressView(LoginRequiredMixin, View):
    '''用户中心-地址页'''

    def get(self, request):
        '''
        显示
        :param request:
        :return: 用户地址页
        '''
        # 获取用户的默认收货地址
        user = request.user  # 获取登录用户对应的用户对象

        # 查到返回地址, 查不到返回None
        address = Address.objects.get_default_address(user)

        # 使用模板
        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        '''地址添加'''
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8|9][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理
        user = request.user  # 获取登录用户对应的用户对象

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(
            user=user,
            receiver=receiver,
            addr=addr,
            phone=phone,
            zip_code=zip_code,
            is_default=is_default
        )
        # 返回应答, 刷新地址页面
        return redirect(reverse('user:address'))  # get请求方式
