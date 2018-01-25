# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render, redirect
from django.test import TestCase
import time
# Create your tests here.
from django.views.decorators.csrf import csrf_exempt

from use_car.models import UserCarDetail


@csrf_exempt
def user_car_apply(request):
    """
    处理用车申请
    :param request:
    :return:
    """
    post = request.POST
    begain_time = post.get('begain','')
    end_time = post.get('end','')
    resign = post.get('resign','')
    peo_num = int(post.get('peo_num',0))
    where = post.get('where','')
    apply_peo = post.get('apply_peo','')
    siji = post.get('siji','')
    car_id = int(post.get('car_type',0))
    shenpi = int(post.get('shenpi',0))
    # print begain_time,end_time,resign,peo_num,where,apply_peo,siji,car_id,shenpi
    begain_time = int(time.mktime(time.strptime(begain_time,'%Y-%m-%d')))   # 将时间转化为时间错
    end_time = int(time.mktime(time.strptime(end_time,'%Y-%m-%d')))
    if begain_time < int(time.time()):
        request.session['error'] = u'时间选择错误'
        return redirect('/car/car_apply/')
    if end_time < begain_time:
        request.session['error'] = u'时间区间选择错误'
        return redirect('/car/car_apply/')
    is_ok = UserCarDetail.objects.filter(car_id=car_id, status=1,).exclude(Q(begain_time__gte=end_time)|Q(end_time__lte=begain_time)).exists() # 查找该车有没有被其他人占用

    if is_ok:
        request.session['error'] = u'该车在改时间内已被占用'
        return redirect('/car/car_apply/')

    UserCarDetail.objects.create(user=request.user,car_id=car_id,resign=resign,begain_time=begain_time,end_time=end_time,siji=siji,
                                 peo_num=peo_num,toplace=where,shenpi_id=shenpi,status=0,add_time=int(time.time()))
    return redirect('/car/car_apply/res/')
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
    UserCarDetail.objects.filter(pk=id).update(status=status,yijian=yijian,update_time=int(time.time()))
    return redirect('/car/car_apply/shenpi/')