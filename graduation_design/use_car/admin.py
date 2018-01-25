# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from use_car.models import CarInfo, UserCarDetail


@admin.register(CarInfo)
class CarInfoAdmin(admin.ModelAdmin):
    """
    list_display:在admin后台展示的字段
    fileds：在后台修改时展示的字段 （）内为在同一行
    决定Model的form中展现哪些字段。fields是包括，exclude是排除。
    """
    list_display = ('name','card','status')
    # fields = (('name', 'num'), 'content','status')
    # list_display_links = ('first_name',)
    # readonly_fields = ('password',) # 只可读不可编辑
    # search_fields = ('first_name','login_status','phone') # 可搜索字段
@admin.register(UserCarDetail)
class UserCarDetailAdmin(admin.ModelAdmin):
    """
    list_display:在admin后台展示的字段
    fileds：在后台修改时展示的字段 （）内为在同一行
    决定Model的form中展现哪些字段。fields是包括，exclude是排除。
    """
    list_display = ('user_id','car_id','status')