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
from comment.ajax import time_, Struct, ajax_ok
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

    shenpi = User.objects.filter(user_type=3,status=1,d_id=user.d_id).all()     # 审批人  组长
    return render(request,'leave/leave_apply.html',context={"user":user,"shenpi":shenpi,"error":error})
def leave_apply_res(request):
    """
    请假申请结果页面
    :param request:
    :return:
    """
    user = request.user
    userleave = LeaveDetail.objects.filter(user=user).last()
    name = User.objects.filter(id=userleave.shenpi_id).last().first_name
    return render(request,'leave/leave_apply_result.html',context={"name":name})

def leave_applying(request):
    """
    申请进度页面
    :param request:
    :return:
    """
    user = request.user
    page = int(request.GET.get('page',1))
    objs = LeaveDetail.objects.filter(user_id=user.id).all().order_by('-id')
    if not objs:
        return render(request, 'leave/leave_applying.html', context={"message":1})
    paginator = Paginator(objs, 1)  # 实例化分页对象，每页展示1条记录 **耗时一秒左右**
    total_page = paginator.num_pages  # 总页数
    try:
        obj = paginator.page(page).object_list  # 获取某页对应的记录
    except PageNotAnInteger:
        page = 1
        obj = paginator.page(page).object_list  # 如果页面不是整数，取第一页的记录
    except EmptyPage:
        page = paginator.num_pages
        obj = paginator.page(paginator.num_pages).object_list  # 如果页码太大， 取最后一页记录
    shenpi = User.objects.filter(id=obj[0].sp_id).last().first_name
    time1, time2 = time_(obj[0],True)
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
    all = LeaveDetail.objects.filter(user_id=uid).all().order_by('-id')
    data = []
    for i in all:
        shenpi = User.objects.filter(id=i.shenpi_id).last().first_name
        time1,time2,time3 = time_(i)
        yijian = i.yijian if i.yijian else ''
        data.append(dict(name=i.user.first_name,time1=time1,time2=time2, where=i.toplace,time=time3,
                         status=int(i.status),leave_name=i.leave.name,num=i.peo_num,shenpi=shenpi,yijian=yijian,
                         resign=i.resign,leave_leaved=i.leave.leaved,
                         ))
    a = '<p style="color:red;">test</p>'
    return render(request,'leave/leave_logs.html',context={"data":data,"test":a})
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
    siji = User.objects.filter(id=my_sp.siji).last().first_name
    shenpi = User.objects.filter(id=my_sp.shenpi_id).last().first_name
    time1, time2, time3 = time_(my_sp)
    data=dict(id=my_sp.id,name=my_sp.user.first_name,time1=time1,time2=time2,siji=siji,shenpi=shenpi,num=my_sp.peo_num,
              resign=my_sp.resign,
              where=my_sp.toplace,leave_name=my_sp.leave.name,leave_leaved=my_sp.leave.leaved)
    return render(request,'leave/leave_shenpi.html',context=data)


@csrf_exempt
def user_leave_apply(request):
    """
    处理用车申请
    :param request:
    :return:
    虽然前段做了空白值处理，后台也要再处理一次防止报错
    """
    post = request.POST
    begain_time = post.get('begain','')
    end_time = post.get('end','')
    resign = post.get('resign','')
    try:# 防止输入天数为中文
        days = float(post.get('days'))
    except:
        request.session['error'] = u'请正确输入请假天数'
        return redirect('/leave/leave_apply/')

    apply_peo = post.get('apply_peo','')   # 暂时用不到的字段
    
    
    shenpi = int(post.get('shenpi',''))
    if not shenpi:
        request.session['error'] = u'请选择审批人'
        return redirect('/leave/leave_apply/')
    # print begain_time,end_time,resign,peo_num,where,apply_peo,siji,leave_id,shenpi
    begain_time = int(time.mktime(time.strptime(begain_time,'%Y-%m-%d')))   # 将时间转化为时间错
    end_time = int(time.mktime(time.strptime(end_time,'%Y-%m-%d')))
    if begain_time < int(time.time()):
        request.session['error'] = u'时间选择错误'
        return redirect('/leave/leave_apply/')
    if end_time < begain_time:
        request.session['error'] = u'时间区间选择错误'
        return redirect('/leave/leave_apply/')


    LeaveDetail.objects.create(user=request.user,resign=resign,begain_time=begain_time,end_time=end_time,
                               days=days,apply_peo=apply_peo,
                                 shenpi_id=shenpi,status=0,add_time=int(time.time()))
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
    LeaveDetail.objects.filter(pk=id).update(status=status,yijian=yijian,update_time=int(time.time()))
    return redirect('/leave/leave_apply/shenpi/')



