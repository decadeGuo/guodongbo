#coding:utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from auth_log.models import User
from comment.ajax import ajax_ok
import time
import datetime
def index(request):
    """
    首页
    error:首页专属错误信息
    type:0 未登录首页（跳转到登录页）  1 登陆后首页
    """
    type = int(request.GET.get('type',0))
    if type == 0:
        error = request.session.get('error')
        request.session['error'] = ''
        return render(request,'auth_log/login.html',context={"error":error})
    else:
        sessionid = request.session.session_key
        return render(request, 'index.html',context={"sessionid":sessionid})
@csrf_exempt
def info(request):
    user = request.user
    position = user.position if user.position else u'暂无职位'
    department = user.depart if user.depart else u'暂无部门'
    time1 = time.strftime("%Y/%m/%d %H:%M", user.last_login.timetuple())  # 上课时间
    data = dict(name=user.first_name, uid=user.id, position1=position,
                department=department, level=user.user_type, time1=time1)
    return ajax_ok(data)
@csrf_exempt
def info_2(request):
    uid = request.POST.get('uid')
    user = User.objects.get(id=uid)
    position = user.position if user.position else u'暂无职位'
    department = user.depart if user.depart else u'暂无部门'
    phone = user.phone
    adress = user.adress
    data = dict(name=user.first_name, uid=user.id, position1=position,
                department=department, level=user.user_type,adress=adress,
                phone=phone)

    return ajax_ok(data)
@csrf_exempt
def not_fond(request):
    return render(request,'404.html')