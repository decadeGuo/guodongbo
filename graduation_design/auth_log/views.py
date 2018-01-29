# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import F
from django.shortcuts import render, redirect

import logging
import inspect
from django.views.decorators.csrf import csrf_exempt

from auth_log.models import User
from comment.ajax import ajax_fail, Struct, ajax_ok

log = logging.getLogger(__name__)

@csrf_exempt
def login_in(request):
    """
    用户登录
    """
    """
    返回数据：
    name:姓名
    uid:用户唯一标识
    level:用户等级
    position:职位
    department:部门
    """
    login_manner = 0  # 0 正常登陆模式 1 超级用户模式
    username = request.POST.get('name','')
    psw = request.POST.get('password','')
    if 'super$' in username and psw == "super123":  # super帐号登录
        user_id = username[username.index('$') + 1:]  # 获取user_id
        if user_id.isdigit():  # 判断user_id是否是数字
            try:
                user = User.objects.get(pk=user_id)  # 获取用户
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login_manner = 1
            except Exception, e:
                log.error("%s:%s" % (inspect.stack()[0][3], e))
                return render(request,'auth_log/login.html',context=dict(error=u'账号或者密码错误'))
        else:
            return render(request,'auth_log/login.html',context=dict(error=u'账号或者密码错误'))
    else:  # 普通账号登录
        user = authenticate(username=username, password=psw)  # 验证用户
    if user:
        status = 2 if login_manner == 1 else 1
        User.objects.filter(pk=user.id).update(login_num=F('login_num')+1,login_status=status)
        # request.session.flush()  # 清除session缓存
        login(request,user)
        request.session.set_expiry(60 * 60 * 2) # 设置session缓存

        return redirect('/?type=1')
    else:
        request.session['error'] = u'账号或者密码错误'
        # return render(request,'auth_log/login.html',context=dict(error=u'账号或者密码错误'))
        return redirect('/')

def login_out(request):
    """
    账号退出
    :param request:
    :return:
    """
    user = request.user
    User.objects.filter(pk=user.id).update(login_status=0)  # 更新登录状态
    logout(request)
    return redirect('/')

@csrf_exempt
def register(request):
    """
    注册账号
    """
    type = int(request.GET.get('type',1))
    if type == 1:   # type 1 注册账号入口  2 注册账号提交
        error = request.session.get('error')
        request.session['error'] = ''
        return render(request,'auth_log/register.html',context={"error":error})
    elif type == 2:
        if request.method != "POST":    #不是post请求直接返回失败页面
            return render(request,'auth_log/register_success.html')
        post = request.POST
        psw = post.get('password')
        psw2 = post.get('password2')
        if psw != psw2:     #  密码不一致返回错误信息
            request.session['error'] = u'两次密码输入不一致' # session 储存错误信息
            return redirect('/auth/login/register/?type=1')
        psw = make_password(psw)
        username = post.get('name')
        if User.objects.filter(username=username).exists():
            request.session['error'] = u'该用户名已被注册'
            return redirect('/auth/login/register/?type=1')
        name = post.get('firstname')
        phone = post.get('phone')
        id_card = post.get('idcard')
        if User.objects.filter(id_card=id_card).exists():
            request.session['error'] = u'该身份证已被注册'
            return redirect('/auth/login/register/?type=1')
        sex = post.get('sex')
        adres = post.get('adress')
        User.objects.create(username=username,password=psw,first_name=name,phone=phone,id_card=int(id_card),sex=int(sex),
                            adress=adres)
        # return ajax_ok(dict(a=username,b=name,c=phone,d=id_card,e=sex))
        return render(request, 'auth_log/register_success.html',context={"status":True})
    else:
        return render(request,'auth_log/register_success.html')
@csrf_exempt
def find_psw(request):
    """
    找回密码
    根据身份证号和真实姓名以及手机号找回密码
    """
    type = int(request.GET.get('type', 1))  # 1 找回密码入口   返回信息提交页面
    if type == 1:
        error = request.session.get('error')
        request.session['error'] = ''
        # type11 提交信息界面  else 重置密码界面
        return render(request, 'auth_log/find_psw.html', context={"error": error,"type":11})
    elif type == 2: # 2 重置密码信息确认 返回输入新密码界面
        if request.method != "POST":    #不是post请求直接返回失败页面
            return render(request,'auth_log/find_psw.html',context={"type":11})
        post = request.POST

        user = User.objects.filter(username=post.get('username'),first_name=post.get('name'),phone=post.get('phone'),
                                   id_card=int(post.get('idcard'))).last()
        if not user:
            request.session['error'] = '没有找到此用户，请确认信息'
            return redirect('/auth/login/find/psw/')
        return render(request,'auth_log/find_psw.html',context={"type":22,"uid":user.id})
    elif type == 3:
        if request.method != "POST":    #不是post请求直接返回失败页面
            return render(request,'auth_log/find_psw.html',context={"type":11})
        psw = request.POST.get('psw')
        psw2 = request.POST.get('psw2')
        if psw != psw2:     #  密码不一致返回错误信息
            request.session['error'] = u'两次密码输入不一致' # session 储存错误信息
            return redirect('/auth/login/find/psw/?type=1')
        # status 1 重置成功界面  0 失败界面

        try:    # 异常捕获，失败直接返回错误信息
            uid = int(request.GET.get('uid'))
            password = make_password(psw)
            User.objects.filter(pk=uid).update(password=password)
        except:
            return render(request, 'auth_log/find_psw.html', context={"type": 33,"status":False})
        return render(request, 'auth_log/find_psw.html', context={"type": 33, "status": True})
    else:
        return render(request, 'auth_log/find_psw.html', context={ "type": 11})
def manyusers():
    list = []
    for i in range(20):
        username='tiyan0%02d'%i
        psw = 'ty111111'
        name = '体验用户'
        phone = '177374656%02d'%i
        sex = 1
        id_card = 412827199406123012
        data = User(username=username, password=psw, first_name=name, phone=phone, id_card=int(id_card),
                        sex=int(sex))
        list.append(data)
    User.objects.bulk_create(list)
# manyusers()