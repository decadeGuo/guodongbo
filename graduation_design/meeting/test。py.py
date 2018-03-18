conding="UTF-8"
import requests
from lxml import etree

url = "https://www.qidian.com/free/all?page=2"
response = requests.get(url)
print response
root = etree.HTML(response.content)
print root
novel_list = root.xpath("//ul/li/div[@class='book-mid-info']/h4/a/text()")
for a in novel_list:
    file = open("C:/Users/Administrator/Desktop/xiaoshuo.txt","w")
    file.write(a)
    file.close()
print 'ok'

# file = open('C:/Users/Administrator/Desktop/xiaoshuo.txt','w')
# file.write('nimen sod')
# file.close()
# print 'ok'