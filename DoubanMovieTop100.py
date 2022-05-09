# coding=utf-8

"""
本程序使用 Python 爬虫抓取豆瓣电影网 TOP100 排行榜（https://movie.douban.com/top250）影片信息，包括电影名称、主演信息、简介
基本步骤：
1.要确定页面类型（静态页面或动态页面）
2.找出页面的 url 规律
3.通过分析网页元素结构来确定正则表达式，从而提取网页信息。

1.静态页面

2.url规律：
https://movie.douban.com/top250
https://movie.douban.com/top250?start=25&filter=
https://movie.douban.com/top250?start=50&filter=
https://movie.douban.com/top250?start=75&filter=

3.元素结构：
                <div class="info">
                    <div class="hd">
                        <a href="https://movie.douban.com/subject/1292052/" class="">
                            <span class="title">肖申克的救赎</span>
                                    <span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>
                                <span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span>
                        </a>


                            <span class="playable">[可播放]</span>
                    </div>
                    <div class="bd">
                        <p class="">
                            导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>
                            1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
                        </p>

                        
                        <div class="star">
                                <span class="rating5-t"></span>
                                <span class="rating_num" property="v:average">9.7</span>
                                <span property="v:best" content="10.0"></span>
                                <span>2613955人评价</span>
                        </div>

                            <p class="quote">
                                <span class="inq">希望让人自由。</span>
                            </p>
                    </div>
                </div>

re = r'<span class="title">(.*?)</span>.*?class="">(.*?)<br>.*?lass="inq">(.*?)</span>'
"""

import time,random,csv,re
from urllib import request,parse
from fake_useragent import UserAgent

class DoubanSpider(object):
    # 定义常用变量,比如url或计数变量等
    def __init__(self):
        self.url = 'https://movie.douban.com/top250?'

    # 获取响应内容函数,使用随机User-Agent
    def get_html(self, url):
        #实例一个随机用户代理
        ua = UserAgent()
        headers = {'User-Agent':ua.chrome}

        #经典三步：获取请求，获取相应，读取html
        req = request.Request(url=url , headers=headers)
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        #print(html)

        return  html

    # 使用正则表达式来解析页面，提取数据
    def parse_html(self, html):
        reg = r'<span class="title">(.*?)</span>.*?class="">(.*?)<br>.*?lass="inq">(.*?)</span>'
        pattern = re.compile(reg, re.S)
        datalist = pattern.findall(html)
        #print('datalist:\n{}'.format(datalist))

        return datalist

    # 将提取的数据按要求保存，csv、MySQL数据库等
    def save_html(self, filename, datalist):
        with open(filename, 'a+', newline='', encoding='utf-8') as f:
            csvfile = csv.writer(f, delimiter=' ',quotechar='|')

            for group in datalist:
                filmname = group[0].strip()
                star = group[1].strip()
                profile = group[2].strip()
                oneline = [filmname, star, profile]

                csvfile.writerow(oneline)

    # 主函数，用来控制整体逻辑
    def run(self):
        start_page  = int(input('请输入起始页\n'))
        end_page    = int(input('请输入结束页\n'))

        #循环爬取指定页数
        for count_page in range(start_page, end_page+1):
            start = (count_page - start_page) * 25
            params = {'start':str(start)}
            params = parse.urlencode(params)
            url = self.url + params
            #print('url:{}\n'.format(url))

            html = self.get_html(url)
            datalist = self.parse_html(html)

            self.save_html('DoubanTop100_{}-{}.csv'.format(start_page,end_page), datalist)

            #适当延时，模拟用户
            '''
            delay_time = random.randint(1, 2)
            print('等待{}s\n'.format(delay_time))
            time.sleep(delay_time)
            '''
            
# 主函数
def main():
    #实例一个爬虫类
    spider = DoubanSpider()

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
























