import time
import datetime

a = "2018/1/20 14:48:27"
b = 1516430907+(60*60*8)
c = time.gmtime(b)
# d=int(time.mktime(time.strptime(a,'%Y/%m/%d %H:%M:%S')))
# print c
# print d
# print time.strptime(a,'%Y/%m/%d %H:%M:%S')
print time.strftime("%Y/%m/%d %H:%M", time.gmtime(b))