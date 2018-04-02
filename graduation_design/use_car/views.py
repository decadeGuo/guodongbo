# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from auth_log.models import User
from comment.ajax import time_, get_shenpi, get_page
from use_car.models import CarInfo, UserCarDetail
import time

def index(request):
    """
    用车主页
    """
    error = request.session.get('error')
    request.session['error']=''
    user_type = request.user.user_type
    apply_num = UserCarDetail.objects.filter(user_id=request.user.id,status=0).count()
    shenpi_num = UserCarDetail.objects.filter(shenpi_id=request.user.id,status=0).count()
    data = dict(user_type=user_type,apply_num=apply_num,shenpi_num=shenpi_num,error=error)
    return render(request, 'car/car_index.html',context=data)
def car_apply(request):
    """
    用车申请页面
    :param request:
    :return:
    """
    error = request.session.get('error')
    request.session['error'] = ''
    user = request.user
    # all_tongyi = UserCarDetail.objects.filter(status=1).all() # 所有已同意的审批
    cars = CarInfo.objects.filter(status=1).all()   # 所有可用车辆
    users = User.objects.filter(user_type__lt=4,status=1).all()  # 司机
    shenpi = get_shenpi(user.d_id)     # 审批人  组长
    return render(request,'car/car_apply.html',context={"user":user,"cars":cars,"users":users,"shenpi":shenpi,"error":error})
def car_apply_res(request):
    """
    用车申请结果页面
    :param request:
    :return:
    """
    user = request.user
    usercar = UserCarDetail.objects.filter(user=user).last()
    name = User.objects.filter(id=usercar.shenpi_id).last().first_name
    return render(request,'car/car_apply_result.html',context={"name":name})
def car_applying(request):
    """
    申请进度页面
    :param request:
    :return:
    """
    user = request.user
    page = int(request.GET.get('page',1))
    objs = UserCarDetail.objects.filter(user_id=user.id).all().order_by('status','-id') # 未审批的排在最前面
    if not objs:
        return render(request, 'car/car_applying.html', context={"message":1})
    obj, page, total_page = get_page(objs, page)
    siji = User.objects.filter(id=obj[0].siji).last().first_name
    shenpi = User.objects.filter(id=obj[0].shenpi_id).last().first_name
    time1, time2, time3 = time_(obj[0],True)
    data = dict(name=obj[0].user.first_name, where=obj[0].toplace, car_name=obj[0].car.name, car_card=obj[0].car.card, siji=siji,
                resign=obj[0].resign,all_num=total_page,current=page
                ,time=time3, shenpi=shenpi, status=int(obj[0].status),id=obj[0].id,page=page,total_page=total_page,time1=time1,time2=time2)
    return render(request,'car/car_applying.html',context=data)
def car_logs(request):
    """
    申请记录页面
    :param request:
    :return:
    """
    uid = request.user.id
    all = UserCarDetail.objects.filter(Q(user_id=uid)|Q(siji=uid)).all().order_by('-id')
    data = []
    for i in all:
        siji = User.objects.filter(id=i.siji).last().first_name
        shenpi = User.objects.filter(id=i.shenpi_id).last().first_name
        time1,time2,time3 = time_(i,True)
        yijian = i.yijian if i.yijian else ''
        data.append(dict(name=i.user.first_name,time1=time1,time2=time2, where=i.toplace,time=time3,
                         status=int(i.status),car_name=i.car.name,num=i.peo_num,siji=siji,shenpi=shenpi,yijian=yijian,
                         resign=i.resign,car_card=i.car.card))
    return render(request,'car/car_logs.html',context={"data":data})
def shenpi(request):
    """
    审批页面
    :param request:
    :return:
    """
    uid = request.user.id
    my_sp = UserCarDetail.objects.filter(shenpi_id=uid,status=0,update_time=0).first()    # 每次审批一个
    if not my_sp:
        my_sp = UserCarDetail.objects.filter(shenpi_id=uid, status=0,update_time__gt=0).first()
        if not my_sp:
            return render(request, 'car/car_shenpi.html',context={"error":1})
    depart = my_sp.user.depart
    siji = User.objects.filter(id=my_sp.siji).last().first_name
    shenpi = User.objects.filter(id=my_sp.shenpi_id).last().first_name
    time1, time2, time3 = time_(my_sp,True)
    data=dict(id=my_sp.id,name=my_sp.user.first_name,time1=time1,time2=time2,siji=siji,shenpi=shenpi,num=my_sp.peo_num,
              resign=my_sp.resign,depart=depart,
              where=my_sp.toplace,car_name=my_sp.car.name,car_card=my_sp.car.card)
    return render(request,'car/car_shenpi.html',context=data)