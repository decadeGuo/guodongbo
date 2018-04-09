#coding:utf-8
"""
未完善的功能：
首页：员工签到
用车：全部用车记录

员工管理：签到详情　　预计新增临时会话
资源管理：论坛资源
消息中心：

预计修改：
审批页面添加当前审批/总审批数
最后一条无法搁置

请假申请处理页面，选择错误后返回保留用户之前输入的内容
其他：员工管理新增已删除的用户展示，可操作为启用

"""

import time
import datetime

a = "2018/1/20 14:48:27"
b = 1516430907+(60*60*8)
c = time.gmtime(b)
# d=int(time.mktime(time.strptime(c,'%Y/%m/%d %H:%M:%S')))
# # print c
# print d
# print time.strptime(a,'%Y/%m/%d %H:%M:%S')
print time.strftime("%Y/%m/%d %H:%M", time.gmtime(1523257767))

month_first_day = datetime.datetime.combine(datetime.date.today().replace(day=1), datetime.time.min)  # 本月第一天
month_first_day = time.strptime(str(month_first_day), '%Y-%m-%d %H:%M:%S')
timestamp = int(time.mktime(month_first_day))
print timestamp
