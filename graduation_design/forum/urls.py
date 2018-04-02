#coding:utf-8
from django.conf.urls import url, include

from forum import views

urlpatterns = [
    url(r'^index/$',views.index),     # 首页
    # url(r'^leave_apply/$', views.leave_apply),  # 请假申请页
    # url(r'^leave_apply/res/$', views.leave_apply_res),  # 用车申请页
    # url(r'^leave_apply/ing/$', views.leave_applying),  # 申请进度页
    # url(r'^leave_apply/logs/$', views.leave_logs),  # 用车申请页
    # url(r'^leave_apply/shenpi/$', views.shenpi),  # 用车审批页

]