# -*- coding: utf-8 -*-

"""
本节使用 Python 爬虫库完成链家二手房（https://bj.lianjia.com/ershoufang/rs/）房源信息抓取，包括楼层、区域、总价、单价等信息。
html解析使用xpath


https://bj.lianjia.com/ershoufang/rs/
https://bj.lianjia.com/ershoufang/pg2/
https://bj.lianjia.com/ershoufang/pg3/
https://bj.lianjia.com/ershoufang/pg4/
"""

import requests
from fake_useragent import UserAgent
from lxml import etree

class LianjiaSpider(object):

    def __init__(self) :
        ua = UserAgent()

        self.url = 'https://bj.lianjia.com/ershoufang/pg{}/'
        self.headers = {'User-Agent':ua.random}
        '''
        /html/body/div[4]/div[1]/ul/li[2]
        /html/body/div[@id='content']/div[@class='leftContent']/ul[@class='sellListContent']/li[@class='clear LOGCLICKDATA'][1]/div[@class='info clear']/div[@class='title']/a
        '''
        
        #self.p_xpath = '/html/body/div[4]/div[1]/ul/li'  # F12定位输出的xpath绝对路径
        #self.p_xpath = '//*[@id="content"]/div[1]/ul/li' # F12定位输出的xpath相对路径  
        #self.p_xpath = '//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]' # xpath helper输出的路径，注意@class属性有触发事件
        self.title_xpath = './/div[@class="info clear"]/div[@class="title"]/a/text()'
        self.locationinfo_xpath = './/div[@class="flood"]/div[@class="positionInfo"]/a[1]/text()'
        self.houseinfo_xpath = './/div[@class="address"]/div[@class="houseInfo"]/text()'
        self.priceinfo_xpath = './/div[@class="priceInfo"]/div[@class="totalPrice totalPrice2"]/span/text()'

    def get_html(self, url):
        res  = requests.get(url=url, headers=self.headers)
        html = res.text 
        print(html)

        return html

    def parse_html(self, html):
        p_html = etree.HTML(html)
        p_list = p_html.xpath(self.p_xpath)
        print(p_list)
        
        item = {}
        for p in p_list:
            # 芍药居北里 满五年南北向 有客厅 诚心出售
            title_list = p.xpath(self.title_xpath)
            item['title'] = title_list[0] if title_list else None

            # 芍药居北里 - 芍药居
            location_list = p.xpath(self.locationinfo_xpath)
            item['location'] = location_list[0] if location_list else None

            # 539
            price_list = p.xpath(self.priceinfo_xpath)
            item['price'] = price_list[0] if price_list else None

            # 2室1厅 | 57.8平米 | 南 北 | 精装 | 中楼层(共7层) | 板楼
            houseinfo_list = p.xpath(self.houseinfo_xpath)
            if houseinfo_list:
                L = houseinfo_list[0].split('|')
                if len(L) >= 6:
                    item['model']    = L[0].strip()
                    item['area']     = L[1].strip()
                    item['direct']   = L[2].strip()
                    item['perfect']  = L[3].strip()
                    item['floor']    = L[4].strip()
                    item['type']     = L[5].strip()

            print(item)
        return item

    def save_info(self):
        pass

    def run(self):
        url = self.url.format('1')
        html = self.get_html(url)
        self.parse_html(html)



def main():
    spider = LianjiaSpider()
    spider.run()

if __name__ == '__main__':
    main()
