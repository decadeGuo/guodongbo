# coding:utf-8
from django.conf.urls import url, include

from forum import views, tests

urlpatterns = [
    url(r'^index/$', views.index),  # 首页
    url(r'^dongtai/$', views.dongtai),  # 广场
    url(r'^me/$', views.me),  # 与我相关
    url(r'^liuyan/$', views.liuyan),  # 留言
    url(r'^zone/$', views.zone)  # 个人中心
]
urlpatterns += [
    url(r'^coll/$', tests.coll),  # 收藏接口
    url(r'^praise/$', tests.praise),  # 点赞接口
    url(r'^add/tag/$', tests.add_tag),  # 点赞接口
]
# 一下是功能路由
urlpatterns += [
    url(r'^article/submit/$',views.article_submit)  # 文章发布提交
]