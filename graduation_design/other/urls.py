#coding:utf-8
from django.conf.urls import url, include

from other import views

urlpatterns = [
    url(r'^index/$',views.index),     # 首页
    url(r'^user/info/$',views.user_info),     # 个人资料
    url(r'^user/manage/$',views.user_manage),     # 个人资料

]
