# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.db.models import Q, F
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from auth_log.models import User
from comment.ajax import Struct
from forum.models import Article, Tags, Coll, Praise, ArticleTalk, LiuYan

now = int(time.time())
def get_res(cs,objs):
    """获取首页查询数据"""
    text = cs.get('text','')
    tag = cs.get('tag','')
    if text and tag:  # 标题内容作者　模糊查询
        filter = Q(title__contains=text)|Q(content__contains=text)|Q(user__first_name__contains=text)
        if int(tag) == -1:  #点赞最多
            res = objs.filter(filter, status=1).all().order_by('-praise')
        elif int(tag) == 0: # 全部
            res = objs.filter(filter, status=1).all().order_by('-add_time')
        else:
            res = objs.filter(filter
                                     ,status=1,tag_id=int(tag)).all().order_by('-add_time')
    elif text:
        res = objs.filter(
            Q(title__contains=text) | Q(content__contains=text) | Q(user__first_name__contains=text)
            , status=1).all().order_by('-add_time')
    elif tag:
        if int(tag) == -1:  #点赞最多
            res = objs.filter(status=1).all().order_by('-praise')
        elif int(tag) == 0: # 全部
            res = objs.filter(status=1).all().order_by('-add_time')
        else:
            res = objs.filter(status=1,tag_id=int(tag)).all().order_by('-add_time')
    else:
        res = objs.filter(status=1).all().order_by('-add_time')
    return res,text,int(tag) if tag else 0


def get_tags():
    """获取分类数据"""
    tags = Tags.objects.filter(status=1).all().order_by('-addtime')
    return tags
def is_coll(id):
    """是否收藏该文章"""
    is_coll = Coll.objects.filter(pk=id).exists()
    return is_coll

def is_praise(id,type):
    """是否点赞了该文章"""
    # type：　１　文章　　２评论　３留言
    is_praise = Praise.objects.filter(pk=id,type=type).exists()
    return is_praise


def get_article_info(res):
    """获取文章的基础信息"""
    data_list = []
    for i in res:
        row = Struct()
        row.id = i.id
        row.title = i.title
        row.content = i.content
        row.auther = i.user.first_name
        row.depart = i.user.depart
        row.tag = i.tag.type
        row.time = time.strftime("%Y/%m/%d", time.gmtime(i.add_time)) # 时间戳转化时间格式
        row.coll = i.coll
        row.praise = i.praise
        row.pl_num = i.pl_num
        row.is_coll = is_coll(i.id)     # 是否收藏
        row.is_praise = is_praise(i.id,1)     # 是否点赞
        row.dp = get_pl(i.id)
        data_list.append(row)

    return data_list

def get_pl(id):
    """获取最佳评论"""
    res = ArticleTalk.objects.filter(aid=id).values('id','content','uid','praise').order_by('-praise')
    res = res[0] if res else {}
    pl_user = User.objects.filter(pk=res.get('id')).last()
    user = pl_user.first_name if pl_user else ''
    depart = pl_user.depart if pl_user else ''
    return dict(id=res.get('id'),content=res.get('content'),praise=res.get('praise'),user=user,depart=depart) if res else {}

def index(request):
    """论坛首页－广场页"""
    cs = request.GET
    objs = Article.objects.filter().all()
    res, text, tag = get_res(cs,objs)
    tags = get_tags()   # 所有的分类
    data_list = get_article_info(res)
    data = dict(text=text,tag=tag,content=data_list,tags=tags)
    # print data
    return render(request,'forum/index.html',context=data)


def dongtai(request):
    """动态页"""
    tags = get_tags()
    message = request.session.get('message')
    request.session['message'] = ''
    return render(request,'forum/dongtai.html',context=dict(message=message,tags=tags))

def me_filter(cs,objs):
    """与我相关页查询函数"""
    text = cs.get('text', '')
    tag = cs.get('tag', '')

    if text and tag:  # 标题内容作者　模糊查询
        filter = Q(title__contains=text)|Q(content__contains=text)|Q(user__first_name__contains=text)
        if int(tag) == -1:  #点赞最多
            res = objs.filter(filter, status=1).all().order_by('-praise')
        elif int(tag) >= 1:
            res = objs.filter(filter,status=1,tag_id=int(tag)).all().order_by('-add_time')
        else:
            res = objs
    elif text:
        res = objs.filter(
            Q(title__contains=text) | Q(content__contains=text) | Q(user__first_name__contains=text)
            , status=1).all().order_by('-add_time')
    elif tag:
        if int(tag) == -1:  #点赞最多
            res = objs.filter(status=1).all().order_by('-praise')
        elif int(tag) >= 1:
            res = objs.filter(status=1,tag_id=int(tag)).all().order_by('-praise')
        else:
            res = objs.filter(status=1).all().order_by('-add_time')

    else:
        res = objs
    return res,text,int(tag) if tag else 0

def me(request):
    """与我相关页"""
    cs = request.GET

    tags = get_tags()
    # 我发布的
    res = Article.objects.filter(user=request.user,status=1).all().order_by('-praise')
    my_articles,text,tag = me_filter(cs,res)
    a_ids = [o.id for o in my_articles]
    # 我评论的id列表(去掉发布的)
    my_pl = list(ArticleTalk.objects.filter(uid=request.user.id).values_list('aid_id',flat=True).exclude(aid_id__in=a_ids))
    my_talk = Article.objects.filter(id__in=my_pl).all()
    my_articles_list = get_article_info(my_articles)
    my_talk_list = get_article_info(my_talk)
    tag = int(cs.get('tag', '0'))

    if tag and int(tag) == -2: # 查看我发布的
        data = dict(tags=tags,article=my_articles_list,tag=tag,text=text)

    elif tag and int(tag) == -3:
        data = dict(tags=tags,pl=my_talk_list,tag=tag,text=text)
    else:
        data = dict(tags=tags, article=my_articles_list, pl=my_talk_list,tag=tag,text=text)
    return render(request,'forum/me.html',context=data)

def liuyan(request):
    """留言页"""
    ly = LiuYan.objects.filter().all().order_by('-praise')  # 查询所有的留言　点赞最多的再前面
    data_list = []
    for o in ly:
        row = {}
        row['name'] = o.user.first_name     # 评论人ＩＤ
        row['depart'] = o.user.depart       # 部门
        row['content'] = o.content
        row['praise'] = o.praise
        row['time'] = time.strftime("%Y/%m/%d", time.gmtime(o.add_time))
        row['is_praise'] = is_praise(o.id,3)    # 是否点赞改留言
        data_list.append(row)
    data = dict(data=data_list)

    return render(request,'forum/liuyan.html',context=data)


def zone(request):
    """个人中心页
    目前版本个中心页显示我的收藏
    """
    cs = request.GET
    tags = get_tags()
    art_ids = list(Coll.objects.filter(uid=request.user.id).values_list('aid',flat=True).order_by('-add_time'))
    res = Article.objects.filter(pk__in=art_ids).all()
    res, text, tag = me_filter(cs, res)
    data_list = get_article_info(res)
    data = dict(tags=tags,data=data_list,text=text,tag=tag)

    return render(request,'forum/zone.html',context=data)

@csrf_exempt
def article_submit(request):
    """
    动态发布提交路由
    """
    post = request.POST
    tag_id = post.get('tag')
    title = post.get('title')
    content = post.get('content')
    if not tag_id:
        message = u'请选择分类'
        tags = get_tags()
        return render(request,'forum/dongtai.html',context=dict(message=message,title=title,content=content,tags=tags))
    try:
        Article.objects.create(title=title,tag_id=int(tag_id),content=content,user=request.user,add_time=now)
        request.session['message'] = u'发布成功'
    except:
        request.session['message'] = u'未知错误'
    return redirect('/forum/dongtai/')
@csrf_exempt
def ly_submit(request):
    """留言提交功能"""
    post = request.POST
    content = post.get('content','')
    LiuYan.objects.create(user=request.user,content=content,praise=0,add_time=now)
    return redirect('/forum/liuyan/')
@csrf_exempt
def pl_submit(request):
    """评论提交功能"""
    post = request.POST
    content = post.get('article_talk','')
    aid = request.GET.get('aid')
    type = request.GET.get('type')
    ArticleTalk.objects.create(uid=request.user.id,content=content,aid_id=aid,add_time=now)
    Article.objects.filter(pk=aid).update(pl_num = F('pl_num') + 1)
    return redirect('/forum/article_deatil/?id=%s&type=%s'%(aid,type))



def article_deatil(request):
    """
    文章详情页
    """
    id = int(request.GET.get('id'))
    type = int(request.GET.get('type'))
    i = Article.objects.filter(pk=id).last()
    row = Struct() # 文章详情
    row.id = i.id
    row.title = i.title
    row.content = i.content
    row.auther = i.user.first_name
    row.depart = i.user.depart
    row.tag = i.tag.type
    row.time = time.strftime("%Y/%m/%d", time.gmtime(i.add_time))  # 时间戳转化时间格式
    row.coll = i.coll
    row.praise = i.praise
    row.pl_num = i.pl_num
    row.is_coll = is_coll(i.id)  # 是否收藏
    row.is_praise = is_praise(i.id, 1)  # 是否点赞

    talk_list = []

    res = ArticleTalk.objects.filter(aid_id=i.id).all().order_by('-praise') # 该文章下面的所有评论
    for o in res:
        tmp = Struct()
        tmp.name = User.objects.filter(pk=o.uid).last().first_name
        tmp.depart = User.objects.filter(pk=o.uid).last().depart
        tmp.content = o.content
        tmp.praise = o.praise
        tmp.time = time.strftime("%Y/%m/%d %H:%M", time.gmtime(o.add_time))  # 时间戳转化时间格式
        talk_list.append(tmp)
    url = '/forum/index/' if type == 0 else '/forum/me/' if type == 1 else '/forum/zone/'
    data = dict(article=row,talk=talk_list,url=url,type=type)
    return render(request,'forum/detail.html',context=data)


