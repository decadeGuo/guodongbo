#coding:utf-8
from django.conf.urls import url, include

from leave import views

urlpatterns = [
    url(r'^index/$',views.index),     # 首页
    url(r'^leave_apply/$', views.leave_apply),  # 请假申请页
    url(r'^leave_apply/res/$', views.leave_apply_res),  # 用车申请页
    url(r'^leave_apply/ing/$', views.leave_applying),  # 申请进度页
    url(r'^leave_apply/logs/$', views.leave_logs),  # 用车申请页
    url(r'^leave_apply/shenpi/$', views.shenpi),  # 用车审批页

]
urlpatterns += [
    # url(r'^applying/$',tests.user_leave_apply),     # 申请提交
    # url(r'^apply/res/$',tests.apply_res),     # 申请提交

]
