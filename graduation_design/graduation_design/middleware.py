#coding:utf-8
import datetime
import logging

from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

from comment.ajax import ajax_fail

nologin_urls = ['/','/admin']
class MyMiddleware(MiddlewareMixin):
    """"""

    def process_request(self, request):
        """
        """
        path = str(request.path)
        if path in nologin_urls:
            pass
        elif path.startswith('/admin/'):
            pass
        elif path.startswith('/auth/'):
            pass
        else:
            user = request.user
            uid = user.id if user else 0
            if not uid:
                return ajax_fail( error=u'会话过期')
    def process_response(self, request, response):
        """解决跨域请求"""
        try:
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
            response["Access-Control-Max-Age"] = "1728000"
        except Exception, e:
            # logging.log.error("process_response1:%s" % e)
            pass
        return response
    def process_exception(self, request, exception):
        """
        功能说明:view函数抛出异常处理
        -------------------------------
        修改人     修改时间
        --------------------------------
        徐威      2013-07-17
        """


        if request.method == "POST":
            return render(request,'404.html')
        return render(request,'404.html')