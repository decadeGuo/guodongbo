# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from auth_log.models import User
class MeetingRoom(models.Model):
    """
    会议室表
    """
    name = models.CharField(max_length=100, default='', verbose_name=u'会议室')
    num = models.IntegerField(default=0, verbose_name=u'容纳人数')
    type = models.IntegerField(default=0, verbose_name=u'类型')  # 1 会议　2 讲座
    status = models.IntegerField(default=1, verbose_name=u'状态')  # -1 删除 0 不可用 1 可用 2已被占用
    add_time = models.IntegerField(default=0)

    class Meta:
        db_table = 'room_info'
        verbose_name = u'车辆表'
class UserMeetRoom(models.Model):
    """
    会议室申请详情表
    """
    #status::[{"uid":1,"status":1,"yijian":"" },]
    user = models.ForeignKey(User)
    room = models.ForeignKey(MeetingRoom)
    resign = models.CharField(max_length=2000,verbose_name=u'原因')
    peo_num = models.IntegerField(default=0,verbose_name=u'人数')

    shenpi_id = models.IntegerField(default=0) # 审批人id
    status = models.CharField(default='',max_length=5000,verbose_name=u'申请状态') # 0 搁置 1 同意 2 不同意
    yijian = models.CharField(default='', max_length=200, verbose_name=u'意见')  # 0 搁置 1 同意 2 不同意
    begain_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    add_time = models.IntegerField(default=0)
    update_time = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_room_detail'
        verbose_name = u'用车表'
