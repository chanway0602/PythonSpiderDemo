# -*- coding: utf-8 -*-

import time,random,csv,re
from urllib import request,parse
from fake_useragent import UserAgent

class DyttSpider(object):
    # 定义常用变量,比如url或计数变量等
    def __init__(self):
        self.one_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
        self.two_url = 'https://www.dytt8.net'
        self.reg1 = r'<td height="26">.*?<a href="(.*?)".*?"ulink">(.*?)</a>'
        self.reg2 = r'<div class="title_all"><h1><font color=#07519a>(.*?)</font></h1></div>.*?<a.*?href="(.*?)".*?>.*?style="BACKGROUND-COLOR:.*?</a>'

    # 获取响应内容函数,使用随机User-Agent
    def get_html(self, url):
        #实例一个随机用户代理
        ua = UserAgent()
        headers = {'User-Agent':ua.chrome}

        #经典三步：获取请求，获取相应，读取html
        req = request.Request(url=url , headers=headers)
        res = request.urlopen(req)
        # 本网站使用gb2312的编码格式
        html = res.read().decode('gb2312', 'ignore')
        #print(html)

        return  html

    # 使用正则表达式来解析页面，提取数据,返回数据列表
    def parse_html(self, reg, html):
        pattern = re.compile(reg, re.S)
        datalist = pattern.findall(html)
        #print('datalist:\n{}'.format(datalist))

        return datalist

    # 将提取的数据按要求保存，csv、MySQL数据库等
    def save_html(self, filename, datalist):
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            csvfile = csv.writer(f, delimiter=' ',quotechar='|')

            for group in datalist:
                filmname = group[0].strip()
                magnet   = group[1].strip()

                oneline = [filmname, magnet]
                csvfile.writerow(oneline)

    # 主函数，用来控制整体逻辑
    def run(self):
        start_page  = int(input('请输入起始页\n'))
        end_page    = int(input('请输入结束页\n'))

        #循环爬取指定页数
        for count_page in range(start_page, end_page+1):
            #一级页面的抓取
            one_url = self.one_url.format(count_page)
            one_html = self.get_html(one_url)
            one_datalist = self.parse_html(self.reg1, one_html)    #[(link, filmname), ...]

            #二级页面的抓取和数据的拼接
            final_data_list = []
            for tmp in one_datalist:
                two_url = self.two_url + tmp[0]
                print('two_url:\n{}'.format(two_url))
                two_html = self.get_html(two_url)
                two_datalist = self.parse_html(self.reg2, two_html)    #[(filmname,magnet)]
                print('two_datalist:\n{}'.format(two_datalist))

                final_data_list.append([two_datalist[0][0], two_datalist[0][1]])

            #保存文件
            self.save_html('DyttMovieMagnet_{}-{}.csv'.format(start_page,end_page), final_data_list)

            #适当延时，模拟用户
            '''
            delay_time = random.randint(1, 2)
            print('等待{}s\n'.format(delay_time))
            time.sleep(delay_time)
            '''
            
# 主函数
def main():
    #实例一个爬虫类
    spider = DyttSpider()

    #计算运行时间
    start_time = time.time()
    try:
        spider.run()
    except Exception as e:
        print('[ERROR]:{}'.format(e))
    end_time   = time.time()
    print('总用时：%.2f' % (end_time - start_time))

# 执行
if __name__ == '__main__':
    main()

