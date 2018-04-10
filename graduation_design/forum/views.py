# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from comment.ajax import Struct
from forum.models import Article, Tags, Coll, Praise


def get_res(cs):
    """获取首页查询数据"""
    text = cs.get('text','')
    tag = cs.get('tag','')
    if text and tag:  # 标题内容作者　模糊查询
        res = Article.objects.filter(Q(title__contains=text)|Q(content__contains=text)|Q(user__first_name__contains=text)
                                     ,status=1,tag_id=int(tag)).all().order_by('add_time')
    elif text:
        res = Article.objects.filter(
            Q(title__contains=text) | Q(content__contains=text) | Q(user__first_name__contains=text)
            , status=1).all().order_by('add_time')
    elif tag:
        res = Article.objects.filter(
            status=1, tag_id=int(tag)).all().order_by('add_time')
    else:
        res = Article.objects.filter(status=1).all().order_by('add_time')
    return res,text,tag


def get_tags():
    """获取分类数据"""
    tags = Tags.objects.filter(status=1).all().order_by('addtime')
    return tags
def is_coll(id):
    """是否收藏该文章"""
    is_coll = Coll.objects.filter(pk=id).exists()
    return is_coll

def is_praise(id):
    """是否点赞了该文章"""
    is_praise = Praise.objects.filter(pk=id).exists()
    return is_praise
def get_article_info(res):
    """获取文章的基础信息"""
    data_list = []
    for i in res:
        row = Struct()
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
        row.is_praise = is_praise(i.id)     # 是否点赞
        data_list.append(row)
    return data_list


def index(request):
    """论坛首页－广场页"""
    cs = request.GET
    res, text, tag = get_res(cs)
    tags = get_tags()   # 所有的分类
    data_list = get_article_info(res)
    data = dict(text=text,tag=tag,content=data_list,tags=tags)
    return render(request,'forum/index.html',context=data)


def dongtai(request):
    """动态页"""
    return render(request,'forum/dongtai.html')
def me(request):
    """与我相关页"""
    return render(request,'forum/me.html')
def liuyan(request):
    """留言页"""
    return render(request,'forum/liuyan.html')
def zone(request):
    """个人中心页"""
    return render(request,'forum/zone.html')