# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F
from django.test import TestCase

# Create your tests here.
import time

from comment.ajax import ajax_ok,ajax_fail
from forum.models import Coll, Praise, Article, ArticleTalk

now = int(time.time())

def coll(request):
    """收藏专用接口
    ajax请求
    """
    aid = request.GET.get('aid')
    uid = request.user.id
    if Coll.objects.filter(uid=uid,aid=aid).exists():
        return ajax_ok(dict(status=0))
    Coll.objects.create(uid=uid,aid=aid,add_time=now)
    return ajax_ok(dict(status=1))

def praise(request):
    """"""
    type = request.GET.get('type')
    uid = request.user.id
    aid = request.get.get('aid')
    status = 0
    num = 0
    if Praise.objects.filter(uid=uid, artcile=int(aid), type=int(type)).exists():
        status = 0
    if int(type) == 1:
        Praise.objects.create(uid=uid, artcile=aid,type=1,num=1)
        status = 1
        Article.objects.filter(pk=aid).update(praise=F('praise')+1)
        num = Article.objects.filter(pk=aid).last().praise
    if int(type) == 2:
        Praise.objects.create(uid=uid, artcile=aid,type=2,num=1)
        status = 1
        ArticleTalk.objects.filter(pk=aid).update(praise=F('praise')+1)
        num = ArticleTalk.objects.filter(pk=aid).last().praise
    return ajax_ok(dict(status=status,num=num))