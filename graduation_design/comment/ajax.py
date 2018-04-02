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
    TO = 60*60*8
    time1 = time.strftime("%Y/%m/%d", time.gmtime(i.begain_time + TO))  # 开始时间
    time2 = time.strftime("%Y/%m/%d", time.gmtime(i.end_time + TO))  # 结束时间
    time3 = time.strftime("%Y/%m/%d %H:%M", time.gmtime(i.add_time + TO))  # 结束时间
    if time_3:
        return time1,time2,time3
    else:
        return time1,time2
def get_shenpi(d_id):
    """获取审批人"""
    return  User.objects.filter(user_type__gte=3, status=1, d_id=d_id).all()  # 审批人  组长