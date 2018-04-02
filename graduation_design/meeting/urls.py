#coding:utf-8
from django.conf.urls import url, include

from meeting import views
urlpatterns = [
    url(r'^index/$',views.index),     # 首页
    url(r'^meeting/apply/$',views.meeting_apply),     # 教室申请
    url(r'^applying/$', views.user_meeting_apply),  # 处理教室申请
    url(r'^apply/res/$', views.meeting_apply_res),  # 教室申请结果页面
    url(r'^meeting/apply/ing/$', views.meeting_applying),  # 申请进度页
    url(r'^meeting/apply/logs/$', views.meeting_logs),  # 申请日志
    url(r'^meeting/apply/shenpi/$', views.shenpi),  # 教室审批页
    url(r'^meeting/apply_res/$', views.apply_res),  # 教室审批结果

]