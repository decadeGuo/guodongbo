# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from auth_log.models import User, Depatment, Position
from comment.ajax import time_, Struct, ajax_ok
from use_car.models import CarInfo, UserCarDetail


def index(request):
    """
    其他首页
    :param request:
    :return:
    """
    return render(request, 'others/other_index.html')


def user_info(request):
    """
    个人资料页面
    :param request:
    :return:
    """

    user = request.user
    sex = u'女' if user.sex == 1 else u'男'
    adress = user.adress if user.adress else u'暂无'
    data = dict(id=user.id, name=user.first_name, sex=sex, phone=user.phone, part=user.depart, position=user.position,
                level=user.user_type, idcard=user.id_card, adress=adress)
    return render(request, 'others/user_info/user_info.html', context=data)


@csrf_exempt
def user_manage(request):
    """
    员工管理首页
    :param request:
    :return:
    """
    request.session['error'] = ''
    content=''
    value=''
    if request.method == 'POST':
        post = request.POST
        search = int(post.get('search'))  # 1id 2姓名 3部门 4职位 5级别 6电话
        content = post.get('search_txt')
        value=search
        try:
            if search == 1:
                res = User.objects.filter(pk=int(content), status=1).all().order_by('-user_type')
            elif search == 2:
                res = User.objects.filter(first_name__contains=content, status=1).all().order_by('-user_type')
            elif search == 3:
                res = User.objects.filter(depart__contains=content, status=1).all().order_by('-user_type')
            elif search == 4:
                res = User.objects.filter(position__contains=content, status=1).all().order_by('-user_type')
            elif search == 5:
                res = User.objects.filter(user_type=int(content), status=1).all().order_by('-user_type')
            elif search == 6:
                res = User.objects.filter(phone__contains=content, status=1).all().order_by('-user_type')
            else:
                res = User.objects.filter(status=1).all().order_by('-user_type')
        except:
            res = User.objects.filter(status=1).all().order_by('-user_type')
            request.session['error'] = '搜索错误，请选择正确组合'
    else:
        res = User.objects.filter(status=1).all().order_by('-user_type')
    if not res:
        request.session['error'] = '无符合条件的内容'
    data = []
    for i in res:
        row = Struct()
        row.id = i.id
        row.name = i.first_name
        row.sex = u'男' if i.sex == 1 else u'女'
        row.depart = i.depart
        row.position = i.position
        row.level = i.user_type
        row.login_num = i.login_num
        row.status = u'在线' if i.login_status == 1 else u'离线'
        row.phone = i.phone
        data.append(row)
    all_depart = Depatment.objects.filter(status=1).all()
    all_position = Position.objects.filter(status=1).all()
    data = {"data": data, "all_d": all_depart, "all_p": all_position, "error": request.session['error'],
            "content":content,"value":value,"p_num":len(data)}
    return render(request, 'others/user_info/user_manage.html', context=data)


@csrf_exempt
def user_manage_update(request):
    """修改员工信息 返回模板
    删除用ajax请求

    """
    if request.method == 'POST':
        post = request.POST
        id = int(post.get('id'))
        name = post.get('name').encode('utf8')
        phone = int(post.get('phone'))
        position = post.get('position')
        depart = post.get('depart')
        level = post.get('level').split('：')[-1]
        p_id = int(position)
        d_id = int(depart)
        adress = post.get('adress')
        if p_id == 0 and d_id != 0:
            d_name = Depatment.objects.filter(pk=d_id).last().name.encode('utf8')
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, d_id=d_id,
                                              depart=d_name, adress=adress)
        elif p_id == 0 and d_id == 0:
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, adress=adress)
        elif p_id != 0 and d_id == 0:
            p_name = Position.objects.filter(pk=p_id).last().name.encode('utf8')
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, p_id=p_id,
                                              position=p_name, adress=adress)
        else:
            d_name = Depatment.objects.filter(pk=d_id).last().name.encode('utf8')
            p_name = Position.objects.filter(pk=p_id).last().name.encode('utf8')
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, p_id=p_id, d_id=d_id,
                                              position=p_name, depart=d_name, adress=adress)
        return redirect('/other/user/manage/')
    else:
        type = int(request.GET.get('type'))
        uid = request.GET.get('uid')

        if type == 1:  # type 1 删除 2 返回签到信息
            User.objects.filter(pk=uid).update(status=-1)
        return ajax_ok()

def ziyuan(request):
    """
    资源管理首页
    :param request:
    :return:
    """
    all_p = Position.objects.filter(status__gte=0).all().order_by('-status')
    all_d = Depatment.objects.filter(status__gte=0).all().order_by('-status')
    return render(request,'others/user_info/ziyuan.html',context={"all_p":all_p,"all_d":all_d})

@csrf_exempt
def add_d_p(request):
    """
    新增部门--职位
    :param request:
    :return:
    """
    post = request.POST
    type = int(post.get('type'))
    title = post.get('title')
    status = int(post.get('status'))
    if type == 1:
        Depatment.objects.create(name=title,status=status)
    else:
        Position.objects.create(name=title,status=status)

    return redirect('/other/ziyuan/')
@csrf_exempt
def status(request):
    """
    部门项目的禁用与启用
    :param request:
    :return:
    """
    post = request.POST

    type = post.get('tid')
    psw = post.get('psw')
    password = request.user.password        # 验证管理员密码
    res = check_password(psw,password)
    if not res:
        return ajax_ok(data={"error":u'密码输入错误',"status":0})

    if int(type[0]) == 2: # 参数混淆传递后台区分

        p = Position.objects.filter(pk=type[1:]).last()
        if int(p.status) == 1:
            status = 0
        else:
            status = 1
        Position.objects.filter(pk=p.id).update(status=status)
    else:
        d = Depatment.objects.filter(pk=type[1:]).last()
        if int(d.status) == 1:
            status = 0
        else:
            status = 1
        Depatment.objects.filter(pk=d.id).update(status=status)
    return ajax_ok(data={"error":u'',"status":1})




