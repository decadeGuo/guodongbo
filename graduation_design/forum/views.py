# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def index(request):
    """论坛首页－广场页"""

    return render(request,'forum/index.html')
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