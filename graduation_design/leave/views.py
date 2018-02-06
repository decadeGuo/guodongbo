# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from auth_log.models import User, Depatment, Position
from comment.ajax import time_, Struct, ajax_ok
from leave.models import LeaveDetail
from use_car.models import CarInfo, UserCarDetail


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
    # all_tongyi = UserCarDetail.objects.filter(status=1).all() # 所有已同意的审批

    shenpi = User.objects.filter(user_type=3,status=1,d_id=user.d_id).all()     # 审批人  组长
    return render(request,'leave/leave_apply.html',context={"user":user,"shenpi":shenpi,"error":error})
def leave_apply_res(request):
    """
    用车申请结果页面
    :param request:
    :return:
    """
    user = request.user
    usercar = LeaveDetail.objects.filter(user=user).last()
    name = User.objects.filter(id=usercar.shenpi_id).last().first_name
    return render(request,'leave/leave_apply_result.html',context={"name":name})








