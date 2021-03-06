#coding:utf-8
from django.conf.urls import url, include

from other import views

urlpatterns = [
    url(r'^index/$',views.index),     # 首页
    url(r'^user/info/$',views.user_info),     # 个人资料
    url(r'^user/manage/$',views.user_manage),     # 员工原理
    url(r'^user/manage/update/$',views.user_manage_update),     # 信息更改
    url(r'^ziyuan/$',views.ziyuan),     # 资源管理页面
    url(r'^car/manage/$',views.car_manage),     # 资源管理页面
    url(r'^room/manage/$',views.room_manage),     # 教室管理
    url(r'^sign/$',views.qiandao),     # 教室管理
]
urlpatterns += [
    url(r'^ziyuan/add/$',views.add_d_p),     # 新增职位部门
    url(r'^ziyuan/update/$',views.status),   # 更改部门职位状态
]