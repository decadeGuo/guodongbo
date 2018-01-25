#coding:utf-8
from django.conf.urls import url, include

from use_car import views, tests

urlpatterns = [
    url(r'^index/$',views.index),     # 登录
    url(r'^car_apply/$', views.car_apply),  # 用车申请页
    url(r'^car_apply/res/$', views.car_apply_res),  # 用车申请页
    url(r'^car_apply/ing/$', views.car_applying),  # 申请进度页
    url(r'^car_apply/logs/$', views.car_logs),  # 用车申请页
    url(r'^car_apply/shenpi/$', views.shenpi),  # 用车审批页

]
urlpatterns += [
    url(r'^applying/$',tests.user_car_apply),     # 申请提交
    url(r'^apply/res/$',tests.apply_res),     # 申请提交

]