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
import time,random
from urllib import request,parse
from fake_useragent import UserAgent

class TiebaSpider(object):
    # 定义常用变量,比如url或计数变量等
    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?'

    # 获取响应内容函数,使用随机User-Agent
    def get_html(self, url):
        #实例一个随机用户代理
        ua = UserAgent()
        headers = {'User-Agent':ua.ie}

        #经典三步：获取请求，获取相应，读取html
        req = request.Request(url=url , headers=headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')

        return  html

    # 使用正则表达式来解析页面，提取数据
    def parse_html(self):
        pass

    # 将提取的数据按要求保存，csv、MySQL数据库等
    def save_html(self, filename, html):
        with  open(filename, 'w') as f:
            f.write(html)

    # 主函数，用来控制整体逻辑
    def run(self):
        start_page  = int(input('请输入起始页\n'))
        end_page    = int(input('请输入结束页\n'))
        search_name = input('请输入要爬取的贴吧名\n')

        #循环爬取指定页数
        for count_page in range(start_page, end_page+1):
            pn = (count_page - start_page) * 50
            params = {'kw':search_name, 'pn':str(pn)}
            params = parse.urlencode(params)
            url = self.url + params
            #print('url:{}\n'.format(url))

            html = self.get_html(url)
            filename = '{}第{}-{}页.html'.format(search_name, count_page, end_page)
            self.save_html(filename, html)
            print('爬取{}第{}页完成\n'.format(search_name, count_page))

            #适当延时，模拟用户
            delay_time = random.randint(1, 2)
            print('等待{}s\n'.format(delay_time))
            time.sleep(delay_time)
            
# 主函数
def main():
    #实例一个爬虫类
    spider = TiebaSpider()

    #计算运行时间
    start_time = time.time()
    spider.run()
    end_time   = time.time()
    print('总用时：%.2f' % (end_time - start_time))

# 执行
if __name__ == '__main__':
    main()







     





















