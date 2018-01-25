# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_log.models import User,Position,Depatment

#  一下两种方法修改站点标题
# class MyAdminSite(admin.AdminSite):
#     site_header = '智能人员管理系统'  # 此处设置页面显示标题
#     site_title = 'Decade管理'  # 此处设置页面头部标题
#
# admin.site = MyAdminSite(name='management')
admin.site.site_header='欢迎使用智能人员管理系统'
admin.site.site_title='Decade管理'
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    list_display:在admin后台展示的字段
    fileds：在后台修改时展示的字段 （）内为在同一行
    决定Model的form中展现哪些字段。fields是包括，exclude是排除。
    """
    list_display = ('first_name','user_type','position','depart','phone','email','login_status','login_num')
    # fields = (('name', 'num'), 'content','status')
    list_display_links = ('first_name',)
    readonly_fields = ('password',) # 只可读不可编辑
    search_fields = ('first_name','login_status','phone') # 可搜索字段

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',) # 可搜索字段
@admin.register(Depatment)
class DepatmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',) # 可搜索字段
# admin.site.register(User,UserAdmin)
# admin.site.register(Position,PositionAdmin)
# admin.site.register(Depatment,DepatmentAdmin)





