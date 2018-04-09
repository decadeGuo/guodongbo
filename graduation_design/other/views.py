# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time,datetime
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from auth_log.models import User, Depatment, Position, UserSign
from comment.ajax import time_, Struct, ajax_ok
from leave.models import LeaveDetail
from use_car.models import CarInfo, UserCarDetail
from meeting.models import MeetingRoom,UserMeetRoom

def index(request):
    """
    其他首页
    :param request:
    :return:
    """
    user_type = int(request.user.user_type)
    return render(request, 'others/other_index.html',context={"user_type":user_type})


def user_info(request):
    """
    个人资料页面
    :param request:
    :return:
    """

    user = request.user
    sex = u'女' if user.sex == 1 else u'男'
    adress = user.adress if user.adress else u'暂无'
    manage = User.objects.filter(d_id=user.d_id,user_type=4).last()    # 主管信息
    zg_name = manage.first_name if manage else '无'
    zg_phone = manage.phone if manage else ''
    zuzhang = User.objects.filter(d_id=user.d_id,user_type=3).last()
    zz_name = zuzhang.first_name if zuzhang else '无'
    zz_phone = zuzhang.phone if zuzhang else ''
    zhuyuan = User.objects.filter(d_id=user.d_id,user_type__lt=3).all()
    zy = ' '.join([o.first_name for o in zhuyuan]) if zhuyuan else ''
    data = dict(id=user.id, name=user.first_name, sex=sex, phone=user.phone, part=user.depart, position=user.position,
                level=user.user_type, idcard=user.id_card, adress=adress,zg_name=zg_name,zg_phone=zg_phone,zz_name=zz_name,
                zz_phone=zz_phone,zy=zy)
    return render(request, 'others/user_info/user_info.html', context=data)


@csrf_exempt
def user_manage(request):
    """
    员工管理首页
    :param request:
    :return:
    """
    request.session['error'] = ''
    content=''
    value=''
    if request.method == 'POST':
        post = request.POST
        search = int(post.get('search'))  # 1id 2姓名 3部门 4职位 5级别 6电话
        content = post.get('search_txt')
        value=search
        try:
            if search == 1:
                res = User.objects.filter(pk=int(content), status=1).all().order_by('-user_type')
            elif search == 2:
                res = User.objects.filter(first_name__contains=content, status=1).all().order_by('-user_type')
            elif search == 3:
                res = User.objects.filter(depart__contains=content, status=1).all().order_by('-user_type')
            elif search == 4:
                res = User.objects.filter(position__contains=content, status=1).all().order_by('-user_type')
            elif search == 5:
                res = User.objects.filter(user_type=int(content), status=1).all().order_by('-user_type')
            elif search == 6:
                res = User.objects.filter(phone__contains=content, status=1).all().order_by('-user_type')
            else:
                res = User.objects.filter(status=1).all().order_by('-user_type')
        except:
            res = User.objects.filter(status=1).all().order_by('-user_type')
            request.session['error'] = '搜索错误，请选择正确组合'
    else:
        res = User.objects.filter(status=1).all().order_by('-user_type')
    if not res:
        request.session['error'] = '无符合条件的内容'
    data = []
    for i in res:
        row = Struct()
        row.id = i.id
        row.name = i.first_name
        row.sex = u'男' if i.sex == 1 else u'女'
        row.depart = i.depart
        row.position = i.position
        row.level = i.user_type
        row.login_num = i.login_num
        row.status = u'在线' if i.login_status == 1 else u'离线'
        row.phone = i.phone
        data.append(row)
    all_depart = Depatment.objects.filter(status=1).all()
    all_position = Position.objects.filter(status=1).all()
    data = {"data": data, "all_d": all_depart, "all_p": all_position, "error": request.session['error'],
            "content":content,"value":value,"p_num":len(data),"user_type":int(request.user.user_type)}
    return render(request, 'others/user_info/user_manage.html', context=data)


@csrf_exempt
def user_manage_update(request):
    """修改员工信息 返回模板
    删除用ajax请求

    """
    if request.method == 'POST':
        post = request.POST
        id = int(post.get('id'))
        name = post.get('name').encode('utf8')
        phone = int(post.get('phone'))
        position = post.get('position')
        depart = post.get('depart')
        level = post.get('level').split('：')[-1]
        print position,depart
        p_id = int(position)
        d_id = int(depart)
        adress = post.get('adress')
        if p_id == 0 and d_id != 0:
            d_name = Depatment.objects.filter(pk=d_id).last().name.encode('utf8')
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, d_id=d_id,
                                              depart=d_name, adress=adress)
        elif p_id == 0 and d_id == 0:
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, adress=adress)
        elif p_id != 0 and d_id == 0:
            p_name = Position.objects.filter(pk=p_id).last().name.encode('utf8')
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, p_id=p_id,
                                              position=p_name, adress=adress)
        else:
            d_name = Depatment.objects.filter(pk=d_id).last().name.encode('utf8')
            p_name = Position.objects.filter(pk=p_id).last().name.encode('utf8')
            User.objects.filter(pk=id).update(first_name=name, phone=phone, user_type=level, p_id=p_id, d_id=d_id,
                                              position=p_name, depart=d_name, adress=adress)
        return redirect('/other/user/manage/')
    else:
        type = int(request.GET.get('type'))
        uid = request.GET.get('uid')

        if type == 1:  # type 1 删除 2 返回签到信息
            User.objects.filter(pk=uid).update(status=-1)
        return ajax_ok()

def ziyuan(request):
    """
    资源管理首页
    :param request:
    :return:
    """
    all_p = Position.objects.filter(status__gte=0).all().order_by('-status')
    all_d = Depatment.objects.filter(status__gte=0).all().order_by('-status')
    return render(request,'others/user_info/ziyuan.html',context={"all_p":all_p,"all_d":all_d})

@csrf_exempt
def add_d_p(request):
    """
    新增部门--职位
    :param request:
    :return:
    """
    post = request.POST
    type = int(post.get('type'))
    title = post.get('title')
    status = int(post.get('status'))
    if type == 1:
        Depatment.objects.create(name=title,status=status)
    else:
        Position.objects.create(name=title,status=status)

    return redirect('/other/ziyuan/')
@csrf_exempt
def status(request):
    """
    部门项目的禁用与启用
    :param request:
    :return:
    """
    post = request.POST

    type = post.get('tid')
    psw = post.get('psw')
    password = request.user.password        # 验证管理员密码
    res = check_password(psw,password)
    if not res:
        return ajax_ok(data={"error":u'密码输入错误',"status":0})

    if int(type[0]) == 2: # 参数混淆传递后台区分

        p = Position.objects.filter(pk=type[1:]).last()
        if int(p.status) == 1:
            status = 0
        else:
            status = 1
        Position.objects.filter(pk=p.id).update(status=status)
    else:
        d = Depatment.objects.filter(pk=type[1:]).last()
        if int(d.status) == 1:
            status = 0
        else:
            status = 1
        Depatment.objects.filter(pk=d.id).update(status=status)
    return ajax_ok(data={"error":u'',"status":1})


def get_cars(res):
    data = []
    for i in res:
        row = Struct()
        row.id = i.get('id')
        row.name = i.get('name')
        row.card = i.get('card')
        row.status = '可用' if i.get('status') == 1 else '已被占用' if i.get('status') == 2 else '不可用'
        row.num = i.get('num')
        row.use_num = UserCarDetail.objects.filter(car_id=row.id).count()
        row.add_time = time.strftime("%Y/%m/%d", time.gmtime(i.get('add_time') + 60 * 60 * 8))
        data.append(row)
    return data

@csrf_exempt
def car_manage(request):
    """
    用车管理页面
    多功能合一
    ｔｙｐｅ 1　删除　２　禁用　３启用　４新增　０　首页 5搜索
    """
    type = int(request.GET.get('type',0))
    # status 0 禁用　１启用　２　正在使用　３删除
    if type == 0:
        if request.method == 'POST':
            post = request.POST
            search = int(post.get('search'))

            search_text = post.get('search_txt')
            try:
                if search == 1:
                    res = CarInfo.objects.filter(pk=int(search_text), status__gte=0).values('id', 'name', 'card', 'num',
                                                                                            'status',
                                                                                            'add_time').order_by(
                        '-status')
                elif search == 2:
                    res = CarInfo.objects.filter(name__icontains=search_text, status__gte=0).values('id', 'name',
                                                                                                    'card', 'num',
                                                                                                    'status',
                                                                                                    'add_time').order_by(
                        '-status')
                elif search == 3:
                    res = CarInfo.objects.filter(card__contains=search_text, status__gte=0).values('id', 'name', 'card',
                                                                                                   'num', 'status',
                                                                                                   'add_time').order_by(
                        '-status')
            except:
                request.session['error'] = '错误'
                return redirect('/other/car/manage/')  # 搜索错误返回首页
            data = get_cars(res)
            return render(request, 'others/user_info/car_manage.html',
                          context={"data": data, "car_num": len(data),"value":search,"content":search_text})
        else:
            error = request.session['error']
            request.session['error'] = ''
            cars = CarInfo.objects.filter(status__gte=0).values('id','name','card','num','status','add_time').order_by('-status')
            data = get_cars(cars)
            return render(request,'others/user_info/car_manage.html',context={"data":data,"car_num":len(data),"error":error})
    if type == 1:

        cid = int(request.POST.get('id'))
        CarInfo.objects.filter(pk=cid).update(status=-1) # 删除
        return ajax_ok()
    if type == 2:
        cid = int(request.POST.get('id'))
        CarInfo.objects.filter(pk=cid).update(status=0)  # 禁用
        return ajax_ok()
    if type == 3:
        cid = int(request.POST.get('id'))
        CarInfo.objects.filter(pk=cid).update(status=1)  # 启用
        return ajax_ok()
    if type == 4:
        post = request.POST
        name = post.get('name')
        card = post.get('card')
        zaizhong = post.get('zaizhong')
        status = post.get('status')
        CarInfo.objects.create(name=name,card=card,num=zaizhong,status=status,add_time=int(time.time()))
        return redirect('/other/car/manage/')
def get_rooms(res):
    data = []
    for i in res:
        row = Struct()
        row.id = i.get('id')
        row.name = i.get('name')
        row.type = '会议' if int(i.get('type')) == 1 else '讲座'
        row.status = '可用' if i.get('status') == 1 else '已被占用' if i.get('status') == 2 else '不可用'
        row.num = i.get('num')
        row.use_num = UserMeetRoom.objects.filter(room_id=row.id).count()
        row.add_time = time.strftime("%Y/%m/%d", time.gmtime(i.get('add_time') + 60 * 60 * 8))
        data.append(row)
    return data

@csrf_exempt
def room_manage(request):
    """
    教室管理页面
    多功能合一
    ｔｙｐｅ 1　删除　２　禁用　３启用　４新增　０　首页 5搜索
    """
    type = int(request.GET.get('type',0))
    # status 0 禁用　１启用　２　正在使用　３删除
    if type == 0:
        if request.method == 'POST':
            post = request.POST
            search = int(post.get('search'))

            search_text = post.get('search_txt')
            try:

                if search == 1:
                    res = MeetingRoom.objects.filter(pk=int(search_text), status__gte=0).values('id', 'name', 'type',
                                                                                            'status','num',
                                                                                            'add_time').order_by(
                        '-status')
                elif search == 2:
                    res = MeetingRoom.objects.filter(name__icontains=search_text, status__gte=0).values('id', 'name',
                                                                                                    'type','num',
                                                                                                    'status',
                                                                                                    'add_time').order_by(
                        '-status')
                elif search == 3:
                    content = 1 if '会议' in search_text else 2
                    res = MeetingRoom.objects.filter(type=content, status__gte=0).values('id', 'name','num',
                                                                                                   'type', 'status',
                                                                                                   'add_time').order_by(
                        '-status')
            except:
                request.session['error'] = '错误'
                return redirect('/other/room/manage/')  # 搜索错误返回首页
            data = get_rooms(res)
            return render(request, 'others/user_info/room_manage.html',
                          context={"data": data, "room_num": len(data),"value":search,"content":search_text})
        else:
            error = request.session['error']
            request.session['error'] = ''
            res = MeetingRoom.objects.filter(status__gte=0).values('id','name','type','num','status','add_time').order_by('-status')
            data = get_rooms(res)
            return render(request,'others/user_info/room_manage.html',context={"data":data,"room_num":len(data),"error":error})
    if type == 1:

        cid = int(request.POST.get('id'))
        MeetingRoom.objects.filter(pk=cid).update(status=-1) # 删除
        return ajax_ok()
    if type == 2:
        cid = int(request.POST.get('id'))
        MeetingRoom.objects.filter(pk=cid).update(status=0)  # 禁用
        return ajax_ok()
    if type == 3:
        cid = int(request.POST.get('id'))
        MeetingRoom.objects.filter(pk=cid).update(status=1)  # 启用
        return ajax_ok()
    if type == 4:
        post = request.POST
        name = post.get('name')
        type = post.get('type')
        zaizhong = post.get('zaizhong') # 容纳人数
        status = post.get('status')
        MeetingRoom.objects.create(name=name,num=zaizhong,type=type,status=status,add_time=int(time.time()))
        return redirect('/other/room/manage/')

def qiandao(request):
    """签到详情接口"""
    uid = request.GET.get('uid')
    #获取当月第一天的时间戳
    month_first_day = datetime.datetime.combine(datetime.date.today().replace(day=1), datetime.time.min)  # 本月第一天
    month_first_day = time.strptime(str(month_first_day), '%Y-%m-%d %H:%M:%S')
    timestamp = int(time.mktime(month_first_day))
    sign = UserSign.objects.filter(uid=uid,addtime__gt=timestamp).all()
    user = User.objects.get(id=uid)
    data_list = []
    for o in sign:
        if o:
            row = {}
            row['name'] = user.first_name
            row['depart'] = user.depart
            row['time'] = time.strftime("%Y/%m/%d %H:%M", time.gmtime(o.addtime + 3600*8))
            row['is_late'] = '是' if o.status == 2 else '否'
            row['num'] = LeaveDetail.objects.filter(user_id=uid,add_time__gt=timestamp).count()
            data_list.append(row)
    return render(request,'others/user_info/sign_detail.html',context=dict(data=data_list))