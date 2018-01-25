#coding:utf-8
from django.conf.urls import url, include
from auth_log import views
urlpatterns = [
    url(r'^index/',views.login_in),     # 登录
    url(r'^login/out/',views.login_out),    # 退出
    url(r'^login/register/',views.register), # 注册
    url(r'^login/find/psw/',views.find_psw), # 找回密码
]
