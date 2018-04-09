#coding:utf-8
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from auth_log.models import User, UserSign
from comment.ajax import ajax_ok
import time
import datetime

import datetime
today = datetime.date.today()
today_time = int(time.mktime(today.timetuple())) # 当天；零点的时间错
def index(request):
    """
    首页
    error:首页专属错误信息111
    type:0 未登录首页（跳转到登录页）  1 登陆后首页
    """
    type = int(request.GET.get('type',0))
    if type == 0:
        error = request.session.get('error')
        request.session['error'] = ''
        return render(request,'auth_log/login.html',context={"error":error})
    else:
        # 获取签到情况
        sign = UserSign.objects.filter(uid=request.user.id,addtime__gt=today_time).last()
        status = 1 if sign else 0
        message='已签到' if sign and sign.status == 1 else '已签到/迟到' if sign and sign.status == 2 else '签到'
        sessionid = request.session.session_key
        return render(request, 'index.html',context={"sessionid":sessionid,"message":message,"status":status})
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

def sign(request):
    """签到"""

    uid = request.user.id

    begain_time = today_time + 86400*9 # 当前九点的时间错
    end_time = today_time + 86400*9 + 86400/2 # 九点半的时间错
    now = int(time.time())
    if UserSign.objects.filter(uid=request.user.id,addtime__gt=today_time).exists():    # 当天已签到的不能再签到
        status=-1
        return ajax_ok(dict(status=status))
    if now>=end_time:
        status = 1
    else:
        status = 2

    UserSign.objects.create(uid=uid,status=status,addtime=now)

    return ajax_ok(dict(status=status))





