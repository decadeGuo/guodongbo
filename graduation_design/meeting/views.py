# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db.models import Q
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from comment.ajax import time_, get_shenpi, get_page
from auth_log.models import User
from meeting.models import MeetingRoom,UserMeetRoom
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    """
    教室首页
    """
    error = request.session.get('error')
    request.session['error'] = ''
    user_type = request.user.user_type
    apply_num = UserMeetRoom.objects.filter(user_id=request.user.id, status=0).count()
    shenpi_num = UserMeetRoom.objects.filter(shenpi_id=request.user.id, status=0).count()
    data = dict(user_type=user_type, apply_num=apply_num, shenpi_num=shenpi_num, error=error)
    return render(request, 'meeting/meeting_index.html', context=data)
def meeting_apply(request):
    """
    教室申请页面
 
    """
    error = request.session.get('error')
    request.session['error'] = ''
    user = request.user
    # all_tongyi = UserleaveDetail.objects.filter(status=1).all() # 所有已同意的审批
    rooms = MeetingRoom.objects.filter(status=1).all()
    shenpi = get_shenpi(user.d_id)     # 获取审批人
    return render(request,'meeting/meeting_apply.html',context={"user":user,"shenpi":shenpi,"error":error,"rooms":rooms})
@csrf_exempt
def meeting_apply_res(request):
    """
    教师申请结果页面
:
    """
    user = request.user
    usermeeting = UserMeetRoom.objects.filter(user=user).last()
    name = User.objects.filter(id=usermeeting.shenpi_id).last().first_name
    return render(request,'meeting/meeting_apply_result.html',context={"name":name})

@csrf_exempt
def user_meeting_apply(request):
    """
    处理教室申请

    虽然前段做了空白值处理，后台也要再处理一次防止报错
    """
    post = request.POST

    begain_time = post.get('begain_time')
    end_time = post.get('end_time')
    resign = post.get('resign','')

    room = post.get('room','')
    if not room:
        request.session['error'] = u'请选择教室，如无可用教室请耐心等待或联系管理员'
        return redirect('/meeting/meeting/apply/')

    shenpi = int(post.get('shenpi',''))
    if not shenpi:
        request.session['error'] = u'请选择审批人'
        return redirect('/meeting/meeting/apply/')

    begain_time = int(time.mktime(time.strptime(begain_time,'%Y-%m-%d')))   # 将时间转化为时间错
    end_time = int(time.mktime(time.strptime(end_time,'%Y-%m-%d')))
    if begain_time < int(time.time()):
        request.session['error'] = u'时间选择错误'
        return redirect('/meeting/meeting/apply/')
    if end_time < begain_time:
        request.session['error'] = u'时间区间选择错误'
        return redirect('/meeting/meeting/apply/')
    is_ok = UserMeetRoom.objects.filter(room_id=int(room), status=1, ).exclude(
        Q(begain_time__gte=end_time) | Q(end_time__lte=begain_time)).exists()  # 查找该车有没有被其他人占用

    if is_ok:
        request.session['error'] = u'该房间在该时间内已被占用'
        return redirect('/meeting/meeting/apply/')

    UserMeetRoom.objects.create(user=request.user,resign=resign,begain_time=begain_time,end_time=end_time,
                               shenpi_id=shenpi,room_id=room,
                                 status=0,add_time=int(time.time()))
    return redirect('/meeting/apply/res/')


def meeting_applying(request):
    """
    申请进度页面
    :param request:
    :return:
    """
    user = request.user
    page = int(request.GET.get('page',1))
    objs = UserMeetRoom.objects.filter(user_id=user.id).all().order_by('status','-id')

    if not objs:
        return render(request, 'meeting/meeting_applying.html', context={"message":1})
    obj,page,total_page = get_page(objs,page)   # 实例化分页对象

    shenpi = User.objects.filter(id=obj[0].shenpi_id).last().first_name
    time1, time2 = time_(obj[0],False)

    data = dict(name=obj[0].user.first_name,depart = user.depart,room=obj[0].room.name,
                resign=obj[0].resign,all_num=total_page
                ,shenpi=shenpi, status=int(obj[0].status),id=obj[0].id,page=page,total_page=total_page,time1=time1,time2=time2)
    return render(request,'meeting/meeting_applying.html',context=data)

def meeting_logs(request):
    """
    申请记录页面
    :param request:
    :return:
    """
    uid = request.user.id
    all = UserMeetRoom.objects.filter(user_id=uid).exclude(status=0).all().order_by('-id')
    data = []
    for i in all:
        shenpi = User.objects.filter(id=i.shenpi_id).last().first_name
        time1,time2,time3 = time_(i,True)
        yijian = i.yijian if i.yijian else ''
        data.append(dict(name=i.user.first_name,time1=time1,time2=time2,time=time3,
                         status=int(i.status),shenpi=shenpi,yijian=yijian,
                         resign=i.resign
                         ))
    return render(request,'meeting/meeting_logs.html',context={"data":data})
def shenpi(request):
    """
    审批页面
    :param request:
    :return:
    """
    uid = request.user.id
    my_sp = UserMeetRoom.objects.filter(shenpi_id=uid,status=0,update_time=0).first()    # 每次审批一个
    if not my_sp:
        my_sp = UserMeetRoom.objects.filter(shenpi_id=uid, status=0,update_time__gt=0).first()
        if not my_sp:
            return render(request, 'meeting/meeting_shenpi.html',context={"error":1})

    shenpi = User.objects.filter(id=my_sp.shenpi_id).last().first_name
    depart = my_sp.user.depart
    time1, time2, time3 = time_(my_sp,True)
    data=dict(id=my_sp.id,name=my_sp.user.first_name,time1=time1,time2=time2,shenpi=shenpi,depart=depart,
              resign=my_sp.resign)
    return render(request,'meeting/meeting_shenpi.html',context=data)
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
    UserMeetRoom.objects.filter(pk=id).update(status=status,yijian=yijian,update_time=int(time.time()))
    return redirect('/meeting/meeting/apply/shenpi/')