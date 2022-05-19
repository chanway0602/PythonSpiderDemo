# -*- coding: utf-8 -*-

"""
本程序通过具体的爬虫程序，演示 BS4 解析库的实际应用。爬虫程序目标：下载诗词名句网（https://www.shicimingju.com/book/）《两晋演义》小说。
"""

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class NovelSpider(object):

    def __init__(self):
        self.url = 'https://www.shicimingju.com{}' # 静态网页
        self.headers = {'User-Agent':UserAgent().random}

    def get_book_info(self):
        html = requests.get(url=self.url.format('/book/liangjinyanyi.html'), headers=self.headers).content #调用content，若用text会乱码
        soup = BeautifulSoup(html, 'lxml')
        novel_list = soup.select('.book-mulu > ul > li > a') # select解析
        item = {}
        for list in novel_list:
            item[list['href']] = list.text # 字典保存章节链接和章节标题
            
        return item

    def save_novel(self):
        item = self.get_book_info()
        with open('《两晋演义》.txt', 'w') as f:
            for k,v in item.items():
                html = requests.get(url=self.url.format(k), headers=self.headers).content #调用content，若用text会乱码
                soup = BeautifulSoup(html, 'lxml')
                artist = soup.find('div', class_='chapter_content').text # find方法查找对应内容
                print('正在下载:-**--%s--**-......' % v)
                f.write(v + '\n' + artist)
                print('结束下载:-**--%s--**-......' % v)
                
def main():
    spider = NovelSpider()
    spider.save_novel()

if __name__ == '__main__':
    main()
