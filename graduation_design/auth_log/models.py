# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
class Position(models.Model):
    """
    职位表
    创建人：Decade
    时间：2018/1/10
    """
    name = models.CharField(default='',max_length=100,verbose_name=u'职位')
    status = models.SmallIntegerField(default=1,verbose_name=u'状态') # 0 默认 1 启用 -1 删除
    class Meta:
        db_table = 'position'
        verbose_name = u'职位表'
class Depatment(models.Model):
    """
    部门
    创建人：Decade
    时间：2018/1/10
    """
    name = models.CharField(default='', max_length=100, verbose_name=u'部门')
    status = models.SmallIntegerField(default=1, verbose_name=u'状态')  # 0 默认 1 启用 -1 删除

    class Meta:
        db_table = 'department'
        verbose_name = u'部门表'

class User(AbstractUser):
    """
    用户拓展表
    创建人：Decade
    时间：2018/1/10
    0 普通员工 1 技术员工 2 更高级 3 小组组长 4 部门主管 5 副总经理 6 CEO 7 总经理 8董事长
    """
    user_type = models.IntegerField(default=0,verbose_name=u'用户级别') # 职位 0 一级 从低到高
    position = models.CharField(max_length=50,default='',verbose_name=u'职位')  # 职位
    depart = models.CharField(max_length=50,default='',verbose_name=u'部门')   # 部门
    sex = models.IntegerField(default=0,verbose_name=u'性别') # 1男 2 女
    phone = models.CharField(max_length=20,default='',verbose_name=u'电话')
    id_card = models.IntegerField(default=0,verbose_name=u'身份证号')
    login_num = models.IntegerField(default=0,verbose_name=u'登录次数')
    login_status = models.SmallIntegerField(default=0,verbose_name=u'登录状态') # 0 未登录 1 已登录 2 超级登录
    p_id = models.IntegerField(default=0,verbose_name=u'职位id')
    d_id = models.IntegerField(default=0, verbose_name=u'部门id')
    status = models.SmallIntegerField(default=1,verbose_name=u'账号状态') # 1 启用 -1 删除
    adress = models.CharField(max_length=200,default='')
    class Meta:
        db_table = 'auth_user'
        verbose_name = u'用户表'
