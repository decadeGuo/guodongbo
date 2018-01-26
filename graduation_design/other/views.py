# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from auth_log.models import User
from comment.ajax import time_
from use_car.models import CarInfo, UserCarDetail
def index(request):
    """
    其他首页
    :param request:
    :return:
    """
    return render(request,'others/other_index.html')
def user_info(request):
    """
    个人资料页面
    :param request:
    :return:
    """



    user = request.user
    sex = u'女' if user.sex == 1 else u'男'
    adress = user.adress if user.adress else u'暂无'
    data = dict(id=user.id,name=user.first_name,sex=sex,phone=user.phone,part=user.depart,position=user.position,
                level=user.user_type,idcard=user.id_card ,adress=adress)
    return render(request,'others/user_info/user_info.html',context=data)