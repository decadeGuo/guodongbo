# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from auth_log.models import User
from meeting.models import MeetingRoom,UserMeetRoom


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
    shenpi = User.objects.filter(user_type=3,status=1,d_id=user.d_id).all()     # 审批人  组长
    return render(request,'meeting/meeting_apply.html',context={"user":user,"shenpi":shenpi,"error":error,"rooms":rooms})
def meeting_apply_res(request):
    """
    请假申请结果页面
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
        request.session['error'] = u'请选择教室，如无可用教室请耐心等待'
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


    UserMeetRoom.objects.create(user=request.user,resign=resign,begain_time=begain_time,end_time=end_time,
                               shenpi_id=shenpi,room_id=room,
                                 status=0,add_time=int(time.time()))
    return redirect('/meeting/apply/res/')
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