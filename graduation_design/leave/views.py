# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from cgitb import html

from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from auth_log.models import User, Depatment, Position
from comment.ajax import time_, Struct, ajax_ok, get_shenpi, get_page
from leave.models import LeaveDetail



def index(request):
    """
    请假首页
    :param request:
    :return:
    """
    error = request.session.get('error')
    request.session['error'] = ''
    user_type = request.user.user_type
    apply_num = LeaveDetail.objects.filter(user_id=request.user.id, status=0).count()
    shenpi_num = LeaveDetail.objects.filter(sp_id=request.user.id, status=0).count()
    data = dict(user_type=user_type, apply_num=apply_num, shenpi_num=shenpi_num, error=error)
    return render(request, 'leave/leave_index.html', context=data)

def leave_apply(request):
    """
    请假申请页面
    :param request:
    :return:
    """
    error = request.session.get('error')
    request.session['error'] = ''
    user = request.user
    # all_tongyi = UserleaveDetail.objects.filter(status=1).all() # 所有已同意的审批

    shenpi = get_shenpi(user.d_id)    # 审批人  组长
    return render(request,'leave/leave_apply.html',context={"user":user,"shenpi":shenpi,"error":error})
def leave_apply_res(request):
    """
    请假申请结果页面
    :param request:
    :return:
    """
    user = request.user
    userleave = LeaveDetail.objects.filter(user=user).last()
    name = User.objects.filter(id=userleave.sp_id).last().first_name
    return render(request,'leave/leave_apply_result.html',context={"name":name})

def leave_applying(request):
    """
    申请进度页面
    :param request:
    :return:
    """
    user = request.user
    page = int(request.GET.get('page',1))
    objs = LeaveDetail.objects.filter(user_id=user.id).all().order_by('status','-id')
    if not objs:
        return render(request, 'leave/leave_applying.html', context={"message":1})
    obj, page, total_page = get_page(objs, page)
    shenpi = User.objects.filter(id=obj[0].sp_id).last().first_name
    time1, time2 = time_(obj[0],False)
    data = dict(name=obj[0].user.first_name,
                resign=obj[0].resign,all_num=total_page
                ,shenpi=shenpi, status=int(obj[0].status),id=obj[0].id,page=page,total_page=total_page,time1=time1,time2=time2)
    return render(request,'leave/leave_applying.html',context=data)
def leave_logs(request):
    """
    申请记录页面
    :param request:
    :return:
    """
    uid = request.user.id
    all = LeaveDetail.objects.filter(user_id=uid).exclude(status=0).all().order_by('-id')
    data = []
    for i in all:
        shenpi = User.objects.filter(id=i.sp_id).last().first_name
        time1,time2,time3 = time_(i,True)
        yijian = i.remark if i.remark else ''
        data.append(dict(name=i.user.first_name,time1=time1,time2=time2,time=time3,
                         status=int(i.status),shenpi=shenpi,yijian=yijian,
                         resign=i.resign
                         ))
    return render(request,'leave/leave_logs.html',context={"data":data})
def shenpi(request):
    """
    审批页面
    :param request:
    :return:
    """
    uid = request.user.id
    my_sp = LeaveDetail.objects.filter(sp_id=uid,status=0,update_time=0).first()    # 每次审批一个
    if not my_sp:
        my_sp = LeaveDetail.objects.filter(sp_id=uid, status=0,update_time__gt=0).first()
        if not my_sp:
            return render(request, 'leave/leave_shenpi.html',context={"error":1})

    shenpi = User.objects.filter(id=my_sp.sp_id).last().first_name
    depart = my_sp.user.depart
    time1, time2, time3 = time_(my_sp,True)
    data=dict(id=my_sp.id,name=my_sp.user.first_name,time1=time1,time2=time2,shenpi=shenpi,days=my_sp.days,depart=depart,
              resign=my_sp.resign)
    return render(request,'leave/leave_shenpi.html',context=data)


@csrf_exempt
def user_leave_apply(request):
    """
    处理请假申请
    :param request:
    :return:
    虽然前段做了空白值处理，后台也要再处理一次防止报错
    """
    post = request.POST

    begain_time = post.get('begain_time')
    end_time = post.get('end_time')
    resign = post.get('resign','')

    try:# 防止输入天数为中文
        days = float(post.get('days'))
    except:
        request.session['error'] = u'请正确输入请假天数'
        return redirect('/leave/leave_apply/')


    shenpi = int(post.get('shenpi',''))
    if not shenpi:
        request.session['error'] = u'请选择审批人'
        return redirect('/leave/leave_apply/')

    begain_time = int(time.mktime(time.strptime(begain_time,'%Y-%m-%d')))   # 将时间转化为时间错
    end_time = int(time.mktime(time.strptime(end_time,'%Y-%m-%d')))
    if begain_time < int(time.time()):
        request.session['error'] = u'时间选择错误'
        return redirect('/leave/leave_apply/')
    if end_time < begain_time:
        request.session['error'] = u'时间区间选择错误'
        return redirect('/leave/leave_apply/')


    LeaveDetail.objects.create(user=request.user,resign=resign,begain_time=begain_time,end_time=end_time,
                               days=days,sp_id=shenpi,
                                 status=0,add_time=int(time.time()))
    return redirect('/leave/leave_apply/res/')
@csrf_exempt
def apply_res(request):
    """
    处理审批
    :param request: 
    :return: 
    """
    post = request.POST
    # print post
    id = int(request.GET.get('id','0'))
    yijian = post.get('yijian','')
    status = post.get('but')
    LeaveDetail.objects.filter(pk=id).update(status=status,remark=yijian,update_time=int(time.time()))
    return redirect('/leave/leave_apply/shenpi/')



