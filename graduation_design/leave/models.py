# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from auth_log.models import User

class LeaveDetail(models.Model):
    """
    请假详情表
    """
    user = models.ForeignKey(User)
    type = models.IntegerField(u'方式',default=1) #　０调休 1事假　２　病假　３婚假
    resign = models.CharField(u'原因',max_length=200,default='')
    days = models.FloatField(u'天数',default=1)
    sp_id = models.IntegerField(u'审批人',default=0)
    begain_time = models.IntegerField(u'开始时间',default=0)
    end_time = models.IntegerField(u'结束时间',default=0)
    status = models.IntegerField(u'审批结果',default=0) # 0提交为同意　１　已同意　２　不同意　－１　删除
    remark = models.CharField(u'拒接原因',default='',max_length=200)
    update_time = models.IntegerField(default=0)
    add_time = models.IntegerField(default=0)
    class Meta:
        db_table = 'leave_detail'
        verbose_name = u'请假详情表'