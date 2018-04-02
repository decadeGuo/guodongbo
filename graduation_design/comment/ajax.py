#coding:utf-8
import json

from django.http import HttpResponse
import time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from auth_log.models import User


def ajax_ok(data='',message='',status='ok'):
    """

    :param data:
    :param message:
    :param status:
    :return:
    """
    data_1 = json.dumps(dict(data=data,message=message,status=status,error=''))
    return HttpResponse(data_1,content_type="application/json")

def ajax_fail(data='',error='',status='fail'):
    """

    :param data:
    :param message:
    :param status:
    :return:
    """
    data_1 = json.dumps(dict(data=data,message='',status=status,error=error))
    return HttpResponse(data_1,content_type="application/json")

class Struct(dict):
    """
    - 为字典加上点语法. 例如:
    >>> o = Struct({'a':1})
    >>> o.a
    >>> 1
    >>> o.b
    >>> None
    """

    def __init__(self, dictobj={}):
        self.update(dictobj)

    def __getattr__(self, name):
        # Pickle is trying to get state from your object, and dict doesn't implement it.
        # Your __getattr__ is being called with "__getstate__" to find that magic method,
        # and returning None instead of raising AttributeError as it should.
        if name.startswith('__'):
            raise AttributeError
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val

    def __hash__(self):
        return id(self)
def time_(i,time_3=False):
    """时间转化　　相差八小时"""
    TO = 60*60*8
    time1 = time.strftime("%Y/%m/%d", time.gmtime(i.begain_time + TO))  # 开始时间
    time2 = time.strftime("%Y/%m/%d", time.gmtime(i.end_time + TO))  # 结束时间
    time3 = time.strftime("%Y/%m/%d %H:%M", time.gmtime(i.add_time + TO))  # 结束时间
    if time_3:
        return time1,time2,time3
    else:
        return time1,time2

def dedupe(items, key=None):
    """
    字典列表去重
    ------------------------------------------------------------------
    修改人         修改时间              修改原因
    ------------------------------------------------------------------
    郭东波          2017-06-09             创建
    :param items:字典列表
    :param key:
    :return:
    """
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
def get_shenpi(d_id):
    """获取审批人"""
    return  User.objects.filter(user_type__gte=3, status=1, d_id=d_id).all()  # 审批人  组长

def get_page(objs,page):
    """分页对象管理"""
    paginator = Paginator(objs, 1)  # 实例化分页对象，每页展示1条记录 **耗时一秒左右**
    total_page = paginator.num_pages  # 总页数
    try:
        obj = paginator.page(page).object_list  # 获取某页对应的记录
    except PageNotAnInteger:
        page = 1
        obj = paginator.page(page).object_list  # 如果页面不是整数，取第一页的记录
    except EmptyPage:
        page = paginator.num_pages
        obj = paginator.page(paginator.num_pages).object_list  # 如果页码太大， 取最后一页记录
    return obj,page,total_page