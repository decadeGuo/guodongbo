#coding:utf-8
from django.conf.urls import url, include

from other import views

urlpatterns = [
    url(r'^index/$',views.index),     # 首页
    url(r'^user/info/$',views.user_info),     # 个人资料
    url(r'^user/manage/$',views.user_manage),     # 员工原理
    url(r'^user/manage/update/$',views.user_manage_update),     # 信息更改

]
