# -*- coding: utf-8 -*-

'''
本程序爬取制定页数的百度图片
'''

import os
import re
from fake_useragent import UserAgent
import requests


class BaiduSpider(object):

    def __init__(self):
        #https://image.baidu.com/search/flip?tn=baiduimage&word=python&pn=40
        self.url = 'https://image.baidu.com/search/flip?'
        self.headers = {'User-Agent':UserAgent().chrome}
        self.reg = '"hoverURL":"(.*?)"'

    def make_params(self, word, pn):
        params = {'word':word, 'pn':pn}

        return params

    def get_html(self, params):

        res = requests.get(self.url, params=params, headers=self.headers)
        html = res.text

        pattern = re.compile(self.reg, re.S)
        img_list = pattern.findall(html)

        return img_list

    def save_img(self, img_list, params):
        filepath = os.getcwd()
        if not os.path.exists(params['word']):
            os.mkdir(params['word'])

        i = 1
        for img_url in img_list:
            res = requests.get(img_url, headers=self.headers)
            img_name = '{}/{}/{}_{}.jpg'.format(filepath, params['word'], params['pn'], i)
            with open(img_name, 'wb') as f:
                f.write(res.content)
            print('{}:下载完成'.format(img_name))
            i += 1

    def run(self):
        search_name = input('请输入要搜索的图片：')
        start_page  = int(input('请输入起始页：'))
        end_page    = int(input('请输入结束页：'))
        
        for count_page in range(start_page, end_page + 1):
            params = self.make_params(search_name, count_page)
            img_list = self.get_html(params)
            self.save_img(img_list, params)

def main():
    spider = BaiduSpider()
    spider.run()

if __name__ == '__main__':
    main()

