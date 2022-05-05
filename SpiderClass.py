# coding=utf-8

'''
本程序使用面向对象的方式编写爬虫
基本框架如下：

# 程序结构
class xxxSpider(object):
    def __init__(self):
        # 定义常用变量,比如url或计数变量等
       
    def get_html(self):
        # 获取响应内容函数,使用随机User-Agent
   
    def parse_html(self):
        # 使用正则表达式来解析页面，提取数据
   
    def write_html(self):
        # 将提取的数据按要求保存，csv、MySQL数据库等
       
    def run(self):
        # 主函数，用来控制整体逻辑
       
if __name__ == '__main__':
    # 程序开始运行时间
    spider = xxxSpider()
    spider.run()
'''

from urllib import request,parse
from fake_useragent import UserAgent

ua = UserAgent()
print(ua.ie)
print(ua.ie)
print(ua.ie)

class TiebaSpider(object):

    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?'

    def get_html(self, url):
        #headers = 
        req = request.Request(url=url , headers=headers)
        res = parse
     





















