# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from auth_log.models import User
class Tags(models.Model):
    """分类表"""
    type=models.CharField(max_length=20)    # 标签内容
    addtime=models.IntegerField(default=0) # 添加时间
    status = models.IntegerField(default=1)  # 1 正常 0 删除
    class Meta:
        db_table = 'forum_tags'
        verbose_name = u'分类表'

class Article(models.Model):
    """
    论坛发表主表
    """
    user = models.ForeignKey(User)  # 作者
    tag = models.ForeignKey(Tags)
    title = models.CharField(max_length=100) # 标题
    content = models.CharField(max_length=5000) # 内容
    praise = models.IntegerField(default=0) # 点赞数量
    coll = models.IntegerField(default=0) # 收藏数量
    zf_num = models.IntegerField(default=0) # 转发数量
    pl_num = models.IntegerField(default=0) # 讨论数量
    add_time = models.IntegerField(default=0)   # 发布时间
    status = models.IntegerField(default=1) # 1 正常 0 删除
    class Meta:
        db_table = 'forum_article'
        verbose_name = u'文章主表'
class ArticleTalk(models.Model):
    """评论表"""
    aid = models.ForeignKey(Article) # 帖子ｉｄ
    content = models.CharField(max_length=1000) # 评论内容
    uid = models.IntegerField(default=0) # 评论人id
    level = models.IntegerField(default=0) # 评论级别 　可楼中楼回复
    l_id = models.IntegerField(default=0)   # 上级评论id
    praise = models.IntegerField(default=0)  #　点赞数
    add_time = models.IntegerField(default=0)   # 评论时间
    class Meta:
        db_table = 'forum_article_talk'
        verbose_name = u'评论表'
class Praise(models.Model):
    """点赞表"""
    type = models.IntegerField(default=0)   #　类型 0 默认　１　文章　２　评论　３　留言
    uid = models.IntegerField(default=0)    # 用户id
    artcile = models.IntegerField(default=0)    # 帖子id　
    num = models.IntegerField(default=0)    # 点赞数
    class Meta:
        db_table = 'forum_article_praise'
        verbose_name = u'点赞表'

class LiuYan(models.Model):
    """留言"""
    user = models.ForeignKey(User)
    content = models.CharField(max_length=500)
    add_time = models.IntegerField(default=0)
    praise = models.IntegerField(default=0)  # 点赞数
    class Meta:
        db_table = 'forum_ly'
        verbose_name = u'留言表'
class Coll(models.Model):
    """收藏表"""
    uid = models.IntegerField(default=0)
    aid = models.IntegerField(default=0)
    add_time = models.IntegerField(default=0)
    class Meta:
        db_table = 'forum_coll'
        verbose_name = u'留言表'













