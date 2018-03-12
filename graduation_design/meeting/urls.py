#coding:utf-8
from django.conf.urls import url, include

from meeting import views
urlpatterns = [
    url(r'^index/$',views.index),     # 首页
    url(r'^meeting/apply/$',views.meeting_apply),     # 教室申请
    url(r'^applying/$', views.user_meeting_apply),  # 处理教室申请
    url(r'^apply/res/$', views.meeting_apply_res),  # 教室申请结果页面
    # url(r'^user/manage/update/$',views.user_manage_update),     # 信息更改
    # url(r'^ziyuan/$',views.ziyuan),     # 资源管理页面
    # url(r'^car/manage/$',views.car_manage),     # 资源管理页面

]